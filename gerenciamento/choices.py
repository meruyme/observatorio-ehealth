class TipoUsuario:
    COORDENADOR = '1'
    ALUNO = '2'

    CHOICES = (
        (COORDENADOR, 'Coordenador'),
        (ALUNO, 'Aluno')
    )


class TipoLocal:
    INTERIOR = '1'
    CAPITAL = '2'

    CHOICES = (
        (INTERIOR, 'Interior'),
        (CAPITAL, 'Capital')
    )


class TipoOrganizacao:
    PUBLICO = '1'
    PRIVADO = '2'
    FEDERAL = '3'

    CHOICES = (
        (PUBLICO, 'Público'),
        (PRIVADO, 'Privado'),
        (FEDERAL, 'Federal')
    )
