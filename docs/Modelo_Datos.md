# Modelo de datos de Alke Wallet

## Entidades
- **Cliente**: perfil relacionado 1:1 con `django.contrib.auth.models.User` mediante `OneToOneField`.
- **Cuenta**: pertenece a un cliente mediante `ForeignKey`; un cliente puede tener muchas cuentas (relación 1:N).
- **Beneficiarios**: relación `ManyToManyField` entre `Cuenta` y `Cliente`; una cuenta puede guardar varios beneficiarios y un cliente puede ser beneficiario de varias cuentas.
- **Transaccion**: relaciona una cuenta origen y una cuenta destino mediante dos claves foráneas a Cuenta.

## Integridad
- Email de Cliente único.
- Número de cuenta único.
- Saldo no negativo y monto positivo mediante validadores y `CheckConstraint`.
- Cuenta de origen distinta de la cuenta de destino.
- `PROTECT` evita borrar clientes/cuentas referenciados por registros financieros.

## Nota de alcance
Proyecto académico; no es una billetera bancaria real. Registrar una transacción no mueve saldos automáticamente. Una implementación financiera real requiere atomicidad, controles de concurrencia, auditoría, idempotencia y revisión de seguridad.
