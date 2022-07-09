import adafruit_dht
import time
import board


class Termometer():
    """
    Esta clase representa un sensor que envia pulsos digitales a un pin GPIO
    conociendo de esta forma las vueltas completas que realiza.

    Mediante el metodo generateWind() se actualizaran los valores de la clase
    calculando y limpiándolos.
    De esta forma queda el modelo para el anemómetro separado de las peticiones
    en tiempo pudiendo pedirse cada una en intervalos distintos se calculará
    siempre la direncia de tiempo dinamicamente.

    La clase quedara siempre tomando datos y se podrán calcular en cualquier
    momento usando para ello los datos recopilados desde la última vez.
    """
    try:
        dht22int = adafruit_dht.DHT22(board.D17)
        temperature_int = dht22int.temperature
        humidity_int = dht22int.humidity

    except RuntimeError as dht_error:
        print(f"Error de Conexion Sensor Interior: {dht_error}")
    try:
        dht22ext = adafruit_dht.DHT22(board.D21)
        temperature_ext = dht22ext.temperature
        humidity_ext = dht22ext.humidity
    except RuntimeError as dht_error:
        print(f"Error de Conexion Sensor Exterior: {dht_error}")

    def __init__(self):

        self.start_read(self.dht22int, self.dht22ext)


    def start_read(self, dht22int, dht22ext):

        fecha_hora = time.strftime("%c")
        self.temperature_int = dht22int.temperature
        self.humidity_int = dht22int.humidity

        self.temperature_ext = dht22ext.temperature
        self.humidity_ext = dht22ext.humidity

        print(f"\n{fecha_hora}")

        # Abrimos archivo donde escribiremos los datos
        data_file = open ('/var/lib/prometheus/node-exporter/datos.prom','w', encoding = 'utf-8')
        #f.write('hola mundo')
        #f.close()

        #si queremos que muestre esto cada 5 segundos descomentar el while y el time.sleep

#print("Dia: "+ time.strftime("%d/%m/%y") + "  Hora: "+ time.strftime("%H:%M:%S"))
        #f.write("Fecha y Hora" + fecha_hora)
#print("Hora: "+ time.strftime("%H:%M:%S+0001"))

        try:
            temp_int = "{:.2f}".format(self.temperature_int)
            data_file.write(f"interior_temp {temp_int}\n")

            print(f"Temperatura Interior= {temp_int} C")

            hum_int = "{:.2f}".format(self.humidity_int)
            data_file.write(f"interior_hum {hum_int}\n")

            print(f"Humedad Interior= {hum_int} %")

        except AttributeError as dht_error:
            print(f"Error del Sensor Interior: {dht_error}")

        try:
            temp_ext = "{:.2f}".format(self.temperature_ext)
            data_file.write(f"exterior_temp {temp_ext}\n")

            print(f"Temperatura Exterior= {temp_ext} C")

            hum_ext = "{:.2f}".format(self.humidity_ext)
            data_file.write(f"exterior_hum {hum_ext}\n")

            print(f"Humedad Exterior= {hum_ext} %")

        except AttributeError as dht_error:
            print(f"Error del Sensor Exterior: {dht_error}")

        # Cerramos el archivo
        data_file.close()

        #time.sleep(5)


