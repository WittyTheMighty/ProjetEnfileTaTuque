from continuumio/miniconda3


COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . .

#Server env
EXPOSE 8080

ENV FLASK_APP=server.app
ENV FLASK_ENV=development
RUN ls
CMD [ "python","-m","flask","run", "--host=0.0.0.0", "--port=8080"]