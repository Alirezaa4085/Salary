نحوه استفاده: دستورالعمل‌های نصب و راه‌اندازی برنامه، اجرای محلی و دسترسی به سیستم:
1.	ترمینال را اجرا میکنیم سپس با دستور زیر پروژه را clone میکنیم.
a.	Git Clone https://github.com/Alirezaa4085/Salari.git
2.	 با دستور زیر وارد دایرکتوری پروژه میشویم.
a.	Cd Salary
3.	سپس یک env میسازیم و آن را اجرا میکنیم.(پیشنهادی)
a.	python3 -m venv <name_of_virtualenv>
b.	<name_of_virtualenv>/scripts/activate
4.	دستور زیر را برای نصب پیشنیاز ها اجرا میکنیم:
a.	pip install -r requarments.txt
5.	دستور زیر را برای اجرای پروژه اجرا میکنیم:
a.	py manage.py runserver
6.	ادرس http://127.0.0.1:8000/ را جهت اجرای پروژه باز میکنیم.
