FROM python:3.12-slim
WORKDIR /MMORPGBoardApp
COPY ./requirements.txt /MMORPGBoardApp/
RUN pip install -r requirements.txt
COPY ./MMORPG_board /MMORPGBoardApp/
CMD ["sh", "-c", "python manage.py migrate &&\
    python manage.py runserver 0.0.0.0:8000"]
EXPOSE 8000