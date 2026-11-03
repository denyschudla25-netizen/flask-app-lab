
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField,
    DecimalField,
    IntegerField,
    FileField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
)

from flask_wtf.file import FileAllowed

class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Введіть ім'я."),
            Length(min=2, max=50)
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть правильну електронну пошту.")
        ]
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("general", "Загальне питання"),
            ("cooperation", "Співпраця"),
            ("support", "Підтримка"),
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(min=10, max=2000)
        ]
    )

    submit = SubmitField("Надіслати")


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(min=3, max=100,
                   message="Назва має містити від 3 до 100 символів.")
        ]
    )

    content = TextAreaField(
        "Опис товару",
        render_kw={"rows": 5, "cols": 40},
        validators=[
            DataRequired(message="Введіть опис товару."),
            Length(min=5, message="Опис має містити щонайменше 5 символів.")
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну."),
            NumberRange(min=0.01, message="Ціна повинна бути більшою за 0.")
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("clothing", "Одяг"),
            ("food", "Продукти"),
            ("other", "Інше"),
        ],
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            DataRequired(message="Введіть кількість."),
            NumberRange(min=0, message="Кількість не може бути від'ємною.")
        ]
    )

    image = FileField(
        "Зображення товару",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Дозволені лише JPG, JPEG та PNG."
            )
        ]
    )

    submit = SubmitField("Зберегти товар")
