import numpy as np
from PyQt5 import QtWidgets, QtCore
import os,sys,logging
import shutil
import tempfile
from proyecto.codigo  import Informe
from proyecto.codigo.estadisticas import Estadistica
from proyecto.codigo.informes.DatosToCsv import DatosToCsv
from proyecto.codigo.informes.ConfiguracionToXML import ConfiguracionToXML

class MediadorPestannas():
    """
    Clase que implementa el mediador de las pestannas.
    
    @var pestannas: instancia del objeto que crea el mediador
    @var estad: creamso obnjeto de la clase estadisticas.
    @var escribeCSV: creamos el objeto que escribira el csv
    @var escribeXML:creamos el objeto que creara el XML
    @var borrar: bandera borrar iniciada a false.
    @var bandera: para detectar cambios inicializada a false.
    
    @author: Ismael Tobar Garcia
    @version: 1.0
    """
    def __init__(self, pestannas):
        """
        Constructor de la clase MediadorPestannas se encargara de inicializar los objetos 
        pasados al constructor y tambien de inicializar las variables y objetos necesarios 
        en el constructor.
        
        @param pestannas: Instancia de la clase que la crea. 
        """
        self.pestannas = pestannas
        self.estad = Estadistica()
        self.escribeCSV = DatosToCsv()
        self.escribeXML = ConfiguracionToXML()
        self.borrar = False
        self.bandera=False


    def inicia_paneles(self):
        """
        Metodo para iniciar los paneles de pestañas.
        """
        self.pestannas.tab1 = QtWidgets.QWidget()
        self.pestannas.tab2 = QtWidgets.QWidget()
        self.pestannas.tab3 = QtWidgets.QWidget()
        
    def tab_1_ui(self):
        """
        Metodo para inicializar el panel de pestañas 1 con todos sus compoenentes.
        """
        self.pestannas.addTab(self.pestannas.tab1, "Lineas pintadas")        
        self.pestannas.button = QtWidgets.QPushButton('Calcular Lineas')
        self.pestannas.button.clicked.connect(self.pestannas.ventana.calcular_lineas)
        self.pestannas.layout_segundo = QtWidgets.QVBoxLayout()      
        self.pestannas.layout_segundo.addWidget(self.pestannas.button)
        self.pestannas.layout_segundo.setAlignment(QtCore.Qt.AlignTop)       
     
    def tab_2_ui(self):
        """
        Metodo para inicializar el panel de pestañas 2 con todos sus compoenentes.
        En este caso tendra muchas mas declaraciones e inicializaciones que en el anterior.
        Tambien se encargara de inicializar los layouts.
        """
        self.pestannas.addTab(self.pestannas.tab2, "Corregir lineas")
        self.pestannas.addTab(self.pestannas.tab3, "Automatico")

        self.pestannas.button2 = QtWidgets.QPushButton('Corregir Lineas')
        self.pestannas.button2.clicked.connect(self.pestannas.corregir_lineas)
        
        self.pestannas.button3 = QtWidgets.QPushButton('Anadir punto')
        self.pestannas.button3.clicked.connect(self.pestannas.anadir_lineas)
        self.pestannas.button3.setEnabled(False)

        self.pestannas.button4 = QtWidgets.QPushButton('Anadir segmentos')
        self.pestannas.button4.clicked.connect(self.pestannas.anadir_puntos)  
        self.pestannas.button4.setEnabled(False)

        self.pestannas.button5 = QtWidgets.QPushButton('Borrar seleccionado')
        self.pestannas.button5.clicked.connect(self.pestannas.borrar_selec)
        
        self.pestannas.button7 = QtWidgets.QPushButton('Guardar tabla')
        self.pestannas.button7.clicked.connect(self.pestannas.guardar_tabla)
        self.pestannas.button7.setEnabled(False)

        self.pestannas.button8 = QtWidgets.QPushButton('Limpiar tabla')
        self.pestannas.button8.clicked.connect(self.pestannas.limpiar_tabla)
        
        self.pestannas.P1 = QtWidgets.QLabel("P_1:")
        self.pestannas.p_2 = QtWidgets.QLabel("P_2:")
        
        self.pestannas.P1_x = QtWidgets.QLabel("0")
        self.pestannas.P1_y = QtWidgets.QLabel("0")
        
        self.pestannas.P2_x = QtWidgets.QLabel("0")
        self.pestannas.P2_y = QtWidgets.QLabel("0")
        
        self.pestannas.table = QtWidgets.QTableWidget(self.pestannas)
        self.pestannas.table.setRowCount(0)
        self.pestannas.table.setColumnCount(4)
        self.pestannas.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pestannas.table.itemSelectionChanged.connect(self.pestannas.selected_row)
        self.pestannas.header = self.pestannas.table.horizontalHeader()
        self.pestannas.header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.pestannas.table.setHorizontalHeaderLabels(['P1X', 'P1Y', 'P2X', 'P2Y'])
      
        self.pestannas.layout_tab_2 = QtWidgets.QHBoxLayout()
        
        self.pestannas.layout_pestanna_1 = QtWidgets.QVBoxLayout()
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button2)
        self.pestannas.layaut_corregir_punto_1 = QtWidgets.QVBoxLayout()
        self.pestannas.layaut_corregir_punto_1.setAlignment(QtCore.Qt.AlignTop)
        self.pestannas.layaut_corregir_punto_1.addWidget(self.pestannas.P1)
        self.pestannas.layout_punto_1 = QtWidgets.QHBoxLayout()
        self.pestannas.layout_punto_1.addWidget(self.pestannas.P1_x)
        self.pestannas.layout_punto_1.addWidget(self.pestannas.P1_y)
        self.pestannas.layout_punto_2 = QtWidgets.QHBoxLayout()
        self.pestannas.layout_punto_2.addWidget(self.pestannas.P2_x)
        self.pestannas.layout_punto_2.addWidget(self.pestannas.P2_y)
        
        self.pestannas.layaut_corregir_punto_1.addLayout(self.pestannas.layout_punto_1)
        self.pestannas.layaut_corregir_punto_1.addWidget(self.pestannas.p_2)
        self.pestannas.layaut_corregir_punto_1.addLayout(self.pestannas.layout_punto_2)
        
        self.pestannas.layout_pestanna_1.addLayout(self.pestannas.layaut_corregir_punto_1)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button3)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button5)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button8)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.table)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button4)
        self.pestannas.layout_pestanna_1.addWidget(self.pestannas.button7)
        self.pestannas.layout_tab_2.addLayout(self.pestannas.layout_pestanna_1)
        
        self.pestannas.tab2.setLayout(self.pestannas.layout_tab_2)    
        self.pestannas.tab1.setLayout(self.pestannas.layout_segundo)
        
    def selected_row(self):
        """
        Metodo correspondiente al listner de la tabla para ver que casilla esta seleccion
        y pintar la correspondiente linea.
        """
        self.pestannas.row_actual = self.pestannas.table.currentRow()
        row = self.pestannas.row_actual
        if row >= 0:
            p1x = self.pestannas.table.item(row, 0)
            p1x = p1x.text()
            p1y = self.pestannas.table.item(row, 1)
            p1y = p1y.text()
            p2x = self.pestannas.table.item(row, 2)
            p2x = p2x.text()
            p2y = self.pestannas.table.item(row, 3)
            p2y = p2y.text()
            self.pestannas.ventana.ax.hold(True) 
            self.pestannas.ventana.ax.set_title('Figura con lineas')
            sel, = self.pestannas.ventana.ax.plot((np.int32(p1x), np.int32(p2x)), (np.int32(p1y) , np.int32(p2y)), 'yellow', linewidth=2.0)
            if self.pestannas.ventana.selec_ante != None:            
                self.pestannas.ventana.ax.lines.remove(self.pestannas.ventana.selec_ante)
            self.pestannas.ventana.selec_ante = sel
            self.pestannas.ventana.ax.hold(False)
            self.pestannas.ventana.canvas.draw()             
            
    def corregir_lineas(self):
        """
        Metodo encargado de la correccion manual de las lineas que hayan quedado sin 
        detectar por nuestro algoritmo.
        """
        self.pestannas.button3.setEnabled(False)
        self.pestannas.p_2.setStyleSheet('color: black')
        self.pestannas.P1.setStyleSheet('color: black')
 
        self.pestannas.P1_x.setText("0")
        self.pestannas.P1_y.setText("0")
        self.pestannas.P2_x.setText("0")
        self.pestannas.P2_y.setText("0")        
        self.pestannas.button2.setEnabled(False)
        coords = []     
        def onclick(event):
            """
            Metodo interno de la funcion anterior que se encargara de obtener las coordenadas
            de los puntos que bayamos clicando.
            
            @param Event: evento que contiene las coordenadas del punto clicado.

            @return: Coordenadas P1 y P2
            """
            ix, iy = event.xdata, event.ydata
            if ix != None and iy != None:
                if len(coords) == 0:
                    self.pestannas.P1.setStyleSheet('color: Red')
                    self.pestannas.P1_x.setText(str(round(ix, 0)))
                    self.pestannas.P1_y.setText(str(round(iy, 0)))
                    coords.append((ix, iy))
                    self.pestannas.ventana.c1 = (ix, iy)
 
                else:
                    self.pestannas.p_2.setStyleSheet('color: Red')
                    self.pestannas.P2_x.setText(str(round(ix, 0)))
                    self.pestannas.P2_y.setText(str(round(iy, 0)))
                    self.pestannas.ventana.c2 = (ix, iy)                    
                    coords.append((ix, iy))
                    self.pestannas.ventana.fig.canvas.mpl_disconnect(cid)
                    self.pestannas.button2.setEnabled(True)
                    self.pestannas.button3.setEnabled(True)
 
            return coords
        cid = self.pestannas.ventana.fig.canvas.mpl_connect('button_press_event', onclick)
        self.pestannas.ventana.canvas.draw()           
         
    def anadir_lineas(self):
        """
        Metodo que se va a encargar de añadir a la imagen la linea que hemso seleccionado 
        manualmente.
        """
        self.bandera=True
        self.pestannas.p_2.setStyleSheet('color: black')
        self.pestannas.P1.setStyleSheet('color: black') 
        self.pestannas.P1_x.setText("0")
        self.pestannas.P1_y.setText("0")
        self.pestannas.P2_x.setText("0")
        self.pestannas.P2_y.setText("0")
        if self.pestannas.ventana.c1 != None and self.pestannas.ventana.c2 != None:        
            row = self.pestannas.table.rowCount()
            self.pestannas.table.insertRow(row)
            self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[0]))))
            self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c1[1]))))
            self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[0]))))
            self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(self.pestannas.ventana.c2[1]))))
            self.pestannas.ventana.tam_segmen_verdad = len(self.pestannas.ventana.lineas)
            self.pestannas.ventana.c1 = None
            self.pestannas.ventana.c2 = None
        self.mostrar_tabla()
        self.pestannas.button3.setEnabled(False)
        item = self.pestannas.table.item(row, 0)
        self.pestannas.table.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)
        self.pestannas.table.selectRow(row)
        self.pestannas.button7.setEnabled(True)
        self.pestannas.ventana.padre.save_file.setEnabled(True) 
         
    def mostrar_tabla(self):
        """
        Metodo que se encargara de mostrar en la imagen las lineas que hay en la tabla
        se llamara desde otras funciones que modifiquen la tabla para asi poder actualizar
        lo que deberia estar en la tabla.
        """
        row = self.pestannas.table.rowCount()
        segmentos = []
        x1, x2, y1, y2 = 0, 0, 0, 0
        for i in range(row):            
            x1 = int(self.pestannas.table.item(i, 0).text())
            x2 = int(self.pestannas.table.item(i, 1).text())
            y1 = int(self.pestannas.table.item(i, 2).text())
            y2 = int(self.pestannas.table.item(i, 3).text())
            segmentos.append(((x1, x2), (y1, y2)))
 
        self.pestannas.ventana.pintar_imagen_y_segmentos(segmentos)
        self.pestannas.ventana.selec_ante = None
        self.pestannas.ventana.canvas.draw()   
                  
    def limpiar_tabla(self):
        """
        Metodo que se va a encargar de limpiar la tabla cuando queramos borrar todo 
        su contenido.        
        """
        for i in reversed(range(self.pestannas.table.rowCount())):
            self.pestannas.table.removeRow(i)
        self.mostrar_tabla()
        self.pestannas.button7.setEnabled(False)
        self.pestannas.ventana.padre.save_file.setEnabled(False)   
                  
    def borrar_selec(self):
        """
        Metodo que se encargfara de borrar la linea o segmento que hemos seleccionado
        previamente dentro de la tabla y sea la que estamos visualizando.
        """
        self.bandera=True
        if self.pestannas.row_actual != -1:
            self.pestannas.table.removeRow(self.pestannas.row_actual)            
            self.pestannas.row_actual = -1
            self.mostrar_tabla()
        if self.pestannas.table.rowCount() > 0:
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
 
        else:
            self.pestannas.button7.setEnabled(False)
            self.pestannas.ventana.padre.save_file.setEnabled(False)
             
    def anadir_puntos(self):
        """
        Metodfo para añadir todos los segmentos calculados por el algoritmo
        que detecta la lineas en rojo dentro de la tabla.
        """
        self.bandera=True
        self.limpiar_tabla()
        row = self.pestannas.table.rowCount()
        if len(self.pestannas.ventana.lineas) != 0:
            for i in self.pestannas.ventana.lineas:
                self.pestannas.table.insertRow(row)
                self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0][0]))))
                self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[0][1]))))
                self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[1][0]))))
                self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[1][1]))))
                row += 1
            self.pestannas.button4.setEnabled(False)
            self.mostrar_tabla()
            self.pestannas.button7.setEnabled(True)
            self.pestannas.ventana.padre.save_file.setEnabled(True)
    
    def msgbtn(self, i):
        """
        Metodo auxiliar para el panel de notificacion o dialogo que nos indica
        si queremos sobreescribir o no el archivo en cuestion.
        
        @param i: informacion del boton que hemos clicado.
        """
        if i.text() == "OK":                      
            self.borrar = True
        else:
            self.borrar = False
                 
    def showdialog(self):
        """
        Metodo que nos muestra el cuadro de dialogo dentro de la aplicacion 
        donde podremos elegir si queremos sobreescribir o no.
        """
        msg = QtWidgets.QMessageBox()
        msg.adjustSize()
        msg.setIcon(QtWidgets.QMessageBox.Warning)    
        msg.setText("La carpeta ya existe")
        msg.setInformativeText("Esta seguro de sobreescribir")
        msg.setWindowTitle("Aviso")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()  # @UnusedVariable

    def guardar_tabla(self):
        """
        Metodo que sirve para guardar los cambios  dentro de la tabla en distintos 
        entregables como por ejemplo un fichero con los estadisticos, otro con la tabla, 
        otro con las lineas detectadas y las dos imagenes original y pintada despues del 
        procesado.
        """
        #Clase PARA LAS estadisticas
        path = QtWidgets.QFileDialog.getExistingDirectory(self.pestannas, "openFolder")
        band=False
        if  path !="":
            if os.path.exists(path+'/Proyecto') :
                self.showdialog()
                if self.borrar ==True:
                    band=True
                else:
                    band=False
            else:
                band=True        
            if band :
                temp = tempfile.mkdtemp()
                temp2 = tempfile.mkdtemp()
                if os.path.exists(path+'/Proyecto'):
                    shutil.copytree(path+'/Proyecto',temp2+'/Proyecto')
                                    
                row = self.pestannas.table.rowCount()
                segmentos=[]
                angulos={}
                long_segmento={}
                lista=[]
                x1,x2,y1,y2=0,0,0,0
                for i in range(row):            
                    x1=int(self.pestannas.table.item(i,0).text())
                    x2=int(self.pestannas.table.item(i,1).text())
                    y1=int(self.pestannas.table.item(i,2).text())
                    y2=int(self.pestannas.table.item(i,3).text())
                    segmentos.append(((x1,x2),(y1,y2)))
                    angulos[((x1,x2),(y1,y2))]=self.estad.angu(((x1,x2),(y1,y2)))
                    long_segmento[((x1,x2),(y1,y2))]=self.estad.longitud_segemento(((x1,x2),(y1,y2)))   
                    
                v,h,md,dm,total=self.estad.clasificar(segmentos,angulos,long_segmento)
           
                st_v,st_h,st_md,st_dm,st_tot,variables_tabla=self.estad.calcular_estadisticas(v, h, md, dm, total)
                lista.extend([v,h,md,dm,st_v,st_h,st_md,st_dm,st_tot])
                self.escribe_proyecto(variables_tabla,temp,temp2,lista,path,segmentos)

            self.bandera=False

    def escribe_proyecto(self,variables_tabla,temp,temp2,lista,path,segmentos):
        """
        Metodo auxiliar para guardar lso entregables delega en el la tarea de escribirlos en la carpeta nueva.
        @param variables_tabla: variables que contiene la tabla.
        @param temp: ruta al fichero temporal.
        @param temp2: ruta al segundo fichero temporal
        @param lista: lista con las variables que escribiremos al csv.
        @param path:Camino donde guardar el Proyecto.
        @param segmentos: segmentos que vamos a pintar y guardar.
        """
        try:
            informe=Informe(variables_tabla,temp)#@UnusedVariable
            self.escribeCSV.guardar(temp, lista)
            self.escribeXML.guardar(temp)
            shutil.copy(self.pestannas.ventana.mediador_ventana.ventana.path, temp+'/Original.jpg')

            self.pestannas.ventana.mediador_ventana.procesado.guardar_y_pintar(self.pestannas.ventana.mediador_ventana.ventana.path,temp, segmentos)                     
             
            if os.path.exists(path+'/Proyecto'):
                shutil.rmtree(path+'/Proyecto')
             
            shutil.copytree(temp,path+'/Proyecto')
            self.pestannas.button7.setEnabled(False)
            self.pestannas.ventana.padre.save_file.setEnabled(False)
    
        except:
            exc="Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
            logging.warning(exc)
            print("Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1]))
            try:
                self.pestannas.button7.setEnabled(True)
                self.pestannas.ventana.padre.save_file.setEnabled(True)
                if os.path.exists(path):
                    shutil.copy(temp2 + '/Proyecto/Original.jpg', path+'/Proyecto/Original.jpg')
                    shutil.copy(temp2 + '/Proyecto/Pintada.jpg', path+'/Proyecto/Pintada.jpg')
                    shutil.copy(temp2 + '/Proyecto/Proyecto.xml', path+'/Proyecto/Proyecto.xml')
                    shutil.copy(temp2 + '/Proyecto/Salida_Estadisticas.csv', path+'/Proyecto/Salida_Estadisticas.csv')
                    shutil.copy(temp2 + '/Proyecto/Salida_Lineas.csv', path+'/Proyecto/Salida_Lineas.csv')
                    shutil.copy(temp2 + '/Proyecto/Tabla.tex', path+'/Proyecto/Tabla.tex')
            except:
                exc="Warning:"+ str(sys.exc_info()[0])+ str(sys.exc_info()[1])
                logging.warning(exc)
        finally:
            shutil.rmtree(temp)  
            shutil.rmtree(temp2) 
        
    def cargar_proyec(self, path):
        """
        Metodo para a partir de un proyecto ecistente carge los ficheros con las lineas calculadas
        dentro de nuestra aplicacion para poder hacer mas o borrar algunas es decir para poder 
        editar los cambios necesarios.
        
        @param path: Camino hasta donde esta nuestro proyecto en custion.
        """
        self.cargado = True
        segmentos = self.escribeCSV.leer(path + '/Salida_Lineas.csv')
        segmentos_procesa = []
        segmentos_pintar = []
        for i in segmentos:
            i = i.replace(' ', '')
            i = i.replace('(', '')
            i = i.replace(')', '')
            i = i.replace(',', ' ')
            segmentos_procesa.append(i.split())
        row = self.pestannas.table.rowCount()
        if len(segmentos_procesa) != 0:
            for i in segmentos_procesa:
                l1, l2 = 0, 0 
                l1 = (i[0], i[1])
                l2 = (i[2], i[3])
                segmentos_pintar.append((l1, l2))                
                self.pestannas.table.insertRow(row)
                self.pestannas.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(int(i[0]))))
                self.pestannas.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(int(i[1]))))
                self.pestannas.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(int(i[2]))))
                self.pestannas.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(int(i[3]))))
                row += 1
                
            self.pestannas.ventana.pintar_imagen_y_segmentos(segmentos_pintar)
            self.pestannas.ventana.selec_ante = None
            self.pestannas.ventana.canvas.draw()