from dataclasses import InitVar, dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum


class OperationStatus(StrEnum):
    SUCCESS = 'УСПЕШНО'
    FAILED = 'ОТКЛОНЕНО'

class OperationType(StrEnum):
    WITHDRAW = "СНЯТИЕ"
    DEPOSIT = "ПОПОЛНЕНИЕ"


@dataclass
class Operation:
    type: OperationType
    amount: Decimal
    status: OperationStatus
    balance: Decimal
    date_time: datetime = field(default_factory=lambda: datetime.now(tz=UTC))

    def __str__(self):
        return (f'тип операции: {self.type.value}, '
                f'сумма: {self.amount}, '
                f'статус: {self.status.value}, '
                f'баланс: {self.balance}, '
                f'время проведения: {self.date_time.strftime("%Y-%m-%d %H:%M:%S")}')


@dataclass  # через датакласс удобнее, мне кажется. Но это субъектиивное мнение.
class Account:
    # счетчик экземпляров класса - счетов
    _account_counter = 1000

    account_holder: InitVar[str]
    balance: InitVar[Decimal] = field(default=Decimal(0))

    def __post_init__(self, account_holder, balance):
        # проверки что все ограничиения соблюдены
        if balance < 0:
            raise ValueError('Баланс не может быть отрицательным.')
        if self._account_counter == 0:
            raise ValueError('Действует огранчениие на количество счетов, обратитесь пожалуйста в поддержку.')


        self.holder = account_holder
        self._account_number = f'ACC-{str(Account._account_counter).zfill(4)}'
        self._balance = balance  # но я бы сделал protected
        self._history: list[Operation] = []  # но я бы сделал protected


        Account._account_counter -= 1
        print(f'Счет для пользователя {self.holder} успешно создан')

    def deposit(self, amount: Decimal) -> None:
        status = OperationStatus.SUCCESS
        try:
            if not isinstance(amount, Decimal) or amount < Decimal('0.01'):
                raise ValueError('Сумма должна быть положительной')  # Тут должна быть наша кастомная ошибка
            self._balance += amount
        except ValueError:
            status = OperationStatus.FAILED
        finally:
            operation = Operation(
                type=OperationType.DEPOSIT,
                amount=amount,
                status=status,
                balance=self._balance
            )
            self._history.append(operation)

    def withdraw(self, amount: Decimal) -> None:
        status = OperationStatus.SUCCESS
        try:
            if amount < Decimal('0.01'):
                raise ValueError('Сумма должна быть положительной')  # Тут должна быть наша кастомная ошибка
            if self._balance - amount < 0:
                raise ValueError('Недостаточно средств')  # Тут должна быть наша кастомная ошибка
            self._balance -= amount
        except ValueError as e:
            print(e)
            status = OperationStatus.FAILED
        finally:
            operation = Operation(
                type=OperationType.WITHDRAW,
                amount=amount,
                status=status,
                balance=self._balance
            )
            self._history.append(operation)

    @property
    def get_balance(self) -> Decimal:
        return self._balance

    def get_history(self) -> None:
        for row in self._history[::-1]:  # обычно в историю если и лезут то за последними операциями
            print(row)



if __name__ == '__main__':
    wallet = Account(account_holder='John Wick')
    print(wallet._account_number)

    wallet.withdraw(Decimal('9.6'))

    print(wallet.get_balance)

    wallet.get_history()

    wallet.deposit(Decimal(15))

    print(wallet.get_balance)

    wallet.get_history()
