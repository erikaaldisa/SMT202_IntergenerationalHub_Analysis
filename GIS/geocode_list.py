import qgis
import csv
import json
import requests
import os

fn ='project\\landmark_output.shp'



postal_code = ['188064','238839','178892','178897']

layerFields = QgsFields()
layerFields.append(QgsField('name',QVariant.String))

webcallURL = "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&searchVal="

writer = QgsVectorFileWriter(fn,'UTF-8',layerFields,QgsWkbTypes.Point,\
QgsCoordinateReferenceSystem('EPSG:3414'),'ESRI Shapefile')

for landmark in postal_code:
    
    webcallUrlCall = webcallURL + landmark

    response =  requests.get(webcallUrlCall)

    results  =  json.loads(response.content.decode('utf-8'))
   
    if(len(results["results"]) != 0):
    
        feat = QgsFeature()
        xCoord = float(results["results"][0]['X'])
        yCoord = float(results["results"][0]['Y'])
        
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(xCoord,yCoord)))
        feat.setAttributes([results["results"][0]['BUILDING']])

        writer.addFeature(feat)
        print(results)
        
        if writer.errorMessage() != '':
            print(writer.errorMessage())
        
        print("Added")
    else:
        print("less than 1 result")

iface.addVectorLayer(fn,'','ogr')
del(writer)
