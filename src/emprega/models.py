from datetime import timedelta

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.utils import timezone

from emprega.validators import validate_cpf, validate_cnpj
from recomendacao.tasks import process_candidato, process_vaga


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class UsuarioNivelChoices(models.IntegerChoices):
    SUPERADMIN = 1, "Super Admin"
    ADMIN = 2, "Administrador"
    EMPREGADOR = 3, "Empregador"
    CANDIDATO = 4, "Candidato"


class SexoChoices(models.IntegerChoices):
    FEMININO = 1, "Feminino"
    MASCULINO = 2, "Masculino"
    NAOINFORMADO = 3, "Não Informado"
    AMBOS = 4, "Ambos"


class EstadoCivilChoices(models.IntegerChoices):
    SOLTEIRO = 1, "Solteiro"
    CASADO = 2, "Casado"
    SEPARADO = 3, "Separado"
    DIVORCIADO = 4, "Divorciado"
    VIUVO = 5, "Viúvo"
    UNIAO_ESTAVEL = 6, "União Estável"
    OUTRO = 7, "Outro"


class IdiomaNivelChoices(models.IntegerChoices):
    BASICO = 1, "Básico"
    INTERMEDIARIO = 2, "Intermediário"
    AVANCADO = 3, "Avançado"
    FLUENTE = 4, "Fluente"
    NATIVO = 5, "Nativo"


class FormacaoNivelChoices(models.IntegerChoices):
    FUNDAMENTAL = 1, "Ensino Fundamental"
    MEDIO = 2, "Ensino Médio"
    SUPERIOR = 3, "Ensino Superior"
    POS_GRADUACAO = 4, "Pós-Graduação"
    MESTRADO = 5, "Mestrado"
    DOUTORADO = 6, "Doutorado"
    POS_DOUTORADO = 7, "Pós-Doutorado"


class JornadaTrabalhoChoices(models.IntegerChoices):
    TEMPO_INTEGRAL = 1, "Tempo Integral"
    TEMPO_PARCIAL = 2, "Tempo Parcial"
    TEMPO_FLEXIVEL = 3, "Tempo Flexível"


class TipoDeficienciaChoices(models.IntegerChoices):
    AUDITIVA = 1, "Auditiva"
    MENTAL = 2, "Mental"
    FISICA = 3, "Física"
    VISUAL = 4, "Visual"
    MULTIPLO = 5, "Múltiplo"
    OUTRO = 6, "Outro"


class ModeloTrabalhoChoices(models.IntegerChoices):
    PRESENCIAL = 1, "Presencial"
    REMOTO = 2, "Remoto"
    HIBRIDO = 3, "Híbrido"


class RegimeContratualChoices(models.IntegerChoices):
    CLT = 1, "CLT"
    PJ = 2, "PJ"
    ESTAGIO = 3, "Estágio"
    TEMPORARIO = 4, "Temporário"
    FREELANCER = 5, "Freelancer"
    VOLUNTARIO = 6, "Voluntário"
    OUTRO = 7, "Outro"


class TokenTypeChoices(models.TextChoices):
    EMAIL_CONFIRMATION = "email_confirmation", "Confirmação de Email"
    PASSWORD_RESET = "password_reset", "Redefinição de Senha"


class UserManager(BaseUserManager):
    def create_user(self, cpf, nome, email, data_nascimento, password):
        if not email:
            raise ValueError("Usuários devem ter um email")

        if not password:
            raise ValueError("Usuários devem ter uma senha")

        if not cpf:
            raise ValueError("Usuários devem ter um CPF")

        if not data_nascimento:
            raise ValueError("Usuários devem ter uma data de nascimento")

        if not nome:
            raise ValueError("Usuários devem ter um nome")

        user = self.model(
            email=self.normalize_email(email),
            cpf=cpf,
            data_nascimento=data_nascimento,
            nome=nome,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, cpf, nome, email, data_nascimento, password):
        user = self.create_user(
            cpf,
            nome,
            email,
            data_nascimento,
            password,
        )
        user.is_superuser = True
        user.nivel_usuario = UsuarioNivelChoices.SUPERADMIN
        user.save()
        return user


class CandidatoManager(models.Manager):
    def get_queryset(self):
        return (
            super(CandidatoManager, self)
            .get_queryset()
            .filter(nivel_usuario=UsuarioNivelChoices.CANDIDATO)
        )


class EmpregadorManager(models.Manager):
    def get_queryset(self):
        return (
            super(EmpregadorManager, self)
            .get_queryset()
            .filter(nivel_usuario=UsuarioNivelChoices.EMPREGADOR)
        )


class Usuario(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    nivel_usuario = models.PositiveSmallIntegerField(
        verbose_name="Nível de Usuário",
        default=UsuarioNivelChoices.CANDIDATO,
        choices=UsuarioNivelChoices.choices,
    )
    nome = models.CharField(verbose_name="Nome completo", max_length=255)
    cpf = models.CharField(
        verbose_name="CPF", max_length=11, unique=True, validators=[validate_cpf]
    )
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    sexo = models.PositiveSmallIntegerField(
        verbose_name="Sexo", null=True, blank=True, choices=SexoChoices.choices
    )
    estado_civil = models.PositiveSmallIntegerField(
        verbose_name="Estado civil",
        null=True,
        blank=True,
        choices=EstadoCivilChoices.choices,
    )
    tipo_deficiencia = models.PositiveSmallIntegerField(
        verbose_name="Tipo de deficiência",
        null=True,
        blank=True,
        choices=TipoDeficienciaChoices.choices,
    )

    atuacao = models.CharField(
        verbose_name="Área de atuação", max_length=255, null=True, blank=True
    )
    cargo = models.CharField(
        verbose_name="Cargo", max_length=255, null=True, blank=True
    )

    email = models.EmailField(verbose_name="E-mail", unique=True)
    telefone = models.CharField(
        verbose_name="Telefone", max_length=14, null=True, blank=True
    )

    foto = models.ImageField(
        verbose_name="Foto", upload_to="fotos", null=True, blank=True
    )
    curriculo = models.FileField(
        verbose_name="Currículo", upload_to="curriculos", null=True, blank=True

    )

    curriculo_processado = models.TextField(verbose_name="Currículo Processado", null=True, blank=True)

    curriculo_embedding = ArrayField(models.FloatField(), blank=True, null=True)

    esta_ativo = models.BooleanField(verbose_name="esta_ativo", default=True)
    esta_verificado = models.BooleanField(verbose_name="esta_verificado", default=False)

    @property
    def is_staff(self):
        return self.nivel_usuario <= UsuarioNivelChoices.ADMIN

    @property
    def empresa(self):
        return Empresa.objects.filter(usuario=self).first()

    @property
    def is_candidato(self):
        return self.nivel_usuario == UsuarioNivelChoices.CANDIDATO

    @property
    def is_empregador(self):
        return self.nivel_usuario == UsuarioNivelChoices.EMPREGADOR

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["nome", "email", "data_nascimento"]

    objects = UserManager()

    def __str__(self):
        return self.nome


class Candidato(Usuario):
    objects = CandidatoManager()

    def save(self, *args, **kwargs):
        from emprega.tasks import send_email_confirmation

        process = kwargs.pop("process", True)
        created = kwargs.pop("created", False)

        super(Usuario, self).save(*args, **kwargs)

        if process and created:
            transaction.on_commit(lambda: process_candidato.delay(pk=self.pk))
            send_email_confirmation.delay('email/confirmar_email.html', self.id)

    class Meta:
        proxy = True
        verbose_name = "Candidato"
        verbose_name_plural = "Candidatos"


class ObjetivoProfissional(AbstractBaseModel):
    cargo = models.CharField(verbose_name="Cargo", max_length=255)
    salario = models.DecimalField(
        verbose_name="Pretensão salarial", max_digits=10, decimal_places=2
    )
    modelo_trabalho = models.PositiveSmallIntegerField(
        verbose_name="Modelo de trabalho", choices=ModeloTrabalhoChoices.choices
    )
    regime_contratual = models.PositiveSmallIntegerField(
        verbose_name="Regime contratual", choices=RegimeContratualChoices.choices
    )
    jornada_trabalho = models.PositiveSmallIntegerField(
        verbose_name="Jornada de trabalho", choices=JornadaTrabalhoChoices.choices
    )

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="objetivo_profissional_usuario"
    )

    def __str__(self):
        return self.usuario.nome


class Idioma(AbstractBaseModel):
    nome = models.CharField(verbose_name="Nome", max_length=255)
    nivel = models.PositiveSmallIntegerField(
        verbose_name="Nível", choices=IdiomaNivelChoices.choices
    )

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="idiomas_usuario"
    )

    def __str__(self):
        return self.nome


class FormacaoAcademica(AbstractBaseModel):
    instituicao = models.CharField(verbose_name="Instituição", max_length=255)
    curso = models.CharField(verbose_name="Curso", max_length=255)
    nivel = models.PositiveSmallIntegerField(
        verbose_name="Nível", choices=FormacaoNivelChoices.choices
    )
    data_inicio = models.DateField(verbose_name="Data de início")
    data_conclusao = models.DateField(verbose_name="Data de conclusão", null=True)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="formacoes_academicas_usuario"
    )

    def __str__(self):
        return self.instituicao + " - " + self.curso


class ExperienciaProfissional(AbstractBaseModel):
    empresa = models.CharField(verbose_name="Empresa", max_length=255)
    cargo = models.CharField(verbose_name="Cargo", max_length=255)
    salario = models.DecimalField(
        verbose_name="Salário", max_digits=10, decimal_places=2, null=True
    )
    atividades = models.TextField(verbose_name="Atividades")
    data_inicio = models.DateField(verbose_name="Data de início")
    data_fim = models.DateField(verbose_name="Data de fim", null=True)

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="experiencias_profissionais_usuario",
    )

    def __str__(self):
        return self.empresa + " - " + self.cargo


class CursoEspecializacao(AbstractBaseModel):
    instituicao = models.CharField(verbose_name="Instituição", max_length=255)
    curso = models.CharField(verbose_name="Curso", max_length=255)
    data_conclusao = models.DateField(verbose_name="Data de conclusão")
    duracao_horas = models.IntegerField(verbose_name="Duração em horas")
    certificado = models.FileField(
        verbose_name="Certificado", null=True, upload_to="certificados"
    )

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="cursos_especializacao_usuario"
    )

    def __str__(self):
        return self.instituicao + " - " + self.curso


class Endereco(AbstractBaseModel):
    cep = models.CharField(verbose_name="CEP", max_length=8, null=True, blank=True)
    logradouro = models.CharField(
        verbose_name="Endereço", max_length=255, null=True, blank=True
    )
    numero = models.CharField(
        verbose_name="Número", max_length=255, null=True, blank=True
    )
    complemento = models.CharField(
        verbose_name="Complemento", max_length=255, null=True, blank=True
    )
    bairro = models.CharField(
        verbose_name="Bairro", max_length=255, null=True, blank=True
    )
    cidade = models.CharField(
        verbose_name="Cidade", max_length=255, null=True, blank=True
    )
    estado = models.CharField(
        verbose_name="Estado", max_length=2, null=True, blank=True
    )


class Empresa(AbstractBaseModel):
    cnpj = models.CharField(
        verbose_name="CNPJ", max_length=14, unique=True, validators=[validate_cnpj]
    )
    razao_social = models.CharField(verbose_name="Razão Social", max_length=255)
    nome_fantasia = models.CharField(verbose_name="Nome Fantasia", max_length=255)
    ramo_atividade = models.CharField(verbose_name="Ramo de atividade", max_length=255)
    numero_funcionarios = models.IntegerField(
        verbose_name="Número de funcionários", null=True, blank=True
    )
    telefone = models.CharField(
        verbose_name="Telefone", max_length=14, null=True, blank=True
    )
    email = models.EmailField(verbose_name="E-mail", unique=True)
    site = models.CharField(verbose_name="Site", max_length=255, null=True, blank=True)

    foto = models.ImageField(
        verbose_name="Foto", upload_to="fotos", null=True, blank=True
    )
    descricao = models.TextField(verbose_name="Descrição", null=True, blank=True)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="empresas_usuario"
    )
    endereco = models.OneToOneField(
        Endereco, on_delete=models.SET_NULL, null=True, related_name="empresa_endereco"
    )

    def __str__(self):
        return self.nome_fantasia


class Beneficio(models.Model):
    nome = models.CharField(verbose_name="Nome", max_length=255)

    def __str__(self):
        return self.nome


class Vaga(AbstractBaseModel):
    cargo = models.CharField(verbose_name="Cargo", max_length=255)
    atividades = models.TextField(verbose_name="Atividades")
    requisitos = models.TextField(verbose_name="Requisitos")
    pessoa_deficiencia = models.BooleanField(
        verbose_name="Pessoa com deficiência", default=False
    )
    salario = models.DecimalField(
        verbose_name="Salário", max_digits=10, decimal_places=2
    )
    jornada_trabalho = models.PositiveSmallIntegerField(
        verbose_name="Jornada de trabalho", choices=JornadaTrabalhoChoices.choices
    )
    modelo_trabalho = models.PositiveSmallIntegerField(
        verbose_name="Modelo de trabalho", choices=ModeloTrabalhoChoices.choices
    )
    regime_contratual = models.PositiveSmallIntegerField(
        verbose_name="Regime contratual", choices=RegimeContratualChoices.choices
    )
    sexo = models.PositiveSmallIntegerField(
        verbose_name="Sexo", choices=SexoChoices.choices
    )
    idade_minima = models.PositiveIntegerField(verbose_name="Idade mínima", default=18)
    idade_maxima = models.PositiveIntegerField(verbose_name="Idade máxima", default=65)
    quantidade_vagas = models.IntegerField(
        verbose_name="Quantidade de vagas", default=1
    )
    esta_ativo = models.BooleanField(verbose_name="Está ativo", default=True)
    beneficios = models.ManyToManyField(Beneficio, related_name="vaga_beneficios")

    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="vagas_empresa"
    )

    vaga_processada = models.TextField(verbose_name="Vaga Processada", null=True, blank=True)

    vaga_embedding = ArrayField(models.FloatField(), blank=True, null=True)

    history = AuditlogHistoryField()

    def save(self, *args, **kwargs):
        process = kwargs.pop("process", True)

        super(Vaga, self).save(*args, **kwargs)

        if process:
            transaction.on_commit(lambda: process_vaga.delay(pk=self.pk))

    def __str__(self):
        return self.cargo


class Candidatura(AbstractBaseModel):
    vaga = models.ForeignKey(
        Vaga, on_delete=models.CASCADE, related_name="candidaturas_vaga"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="candidaturas_usuario"
    )
    esta_ativo = models.BooleanField(verbose_name="Está ativo", default=True)

    class Meta:
        unique_together = ("vaga", "usuario")

    def __str__(self):
        return self.vaga.cargo + " - " + self.usuario.cpf


class Avaliacao(AbstractBaseModel):
    vaga = models.ForeignKey(
        Vaga, on_delete=models.CASCADE, related_name="avaliacoes_vaga"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="avaliacoes_usuario"
    )

    class Meta:
        unique_together = ("vaga", "usuario")

    def __str__(self):
        return self.vaga.cargo + " - " + self.usuario.cpf


class Empregador(Usuario):
    objects = EmpregadorManager()

    @property
    def vagas(self):
        return Vaga.objects.filter(empresa__usuario=self)

    class Meta:
        proxy = True
        verbose_name = "Empregador"
        verbose_name_plural = "Empregadores"

    def save(self, *args, **kwargs):
        from emprega.tasks import send_email_confirmation

        created = kwargs.pop('created', False)

        super(Usuario, self).save(*args, **kwargs)

        if created:
            send_email_confirmation.delay('email/confirmar_email.html', self.id)


class Token(AbstractBaseModel):
    token = models.CharField(max_length=40)
    user = models.OneToOneField(
        Usuario, related_name="auth_token", on_delete=models.CASCADE, null=True, blank=True
    )
    type = models.CharField(max_length=100, choices=TokenTypeChoices.choices)

    def __str__(self):
        return self.token

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._generate_key()
        return super(Token, self).save(*args, **kwargs)

    def _generate_key(self):
        return default_token_generator.make_token(self.user)

    def is_valid(self):
        return self.created_at > (timezone.now() - timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT))

    def check_token(self, token):
        return default_token_generator.check_token(self.user, token)


auditlog.register(Usuario)
auditlog.register(Candidato)
auditlog.register(Empregador)
auditlog.register(Endereco)
auditlog.register(Empresa)
auditlog.register(Vaga)
auditlog.register(Candidatura)
auditlog.register(FormacaoAcademica)
auditlog.register(ObjetivoProfissional)
auditlog.register(Idioma)
auditlog.register(ExperienciaProfissional)
auditlog.register(CursoEspecializacao)
auditlog.register(Avaliacao)
