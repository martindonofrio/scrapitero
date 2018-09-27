# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapPruebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    descripcion = scrapy.Field()
    precio = scrapy.Field()
    codigoZonaProp = scrapy.Field()
    codigoAnunciante = scrapy.Field()
    direccion = scrapy.Field()
    antiguedadAviso = scrapy.Field()
    superficieTotal = scrapy.Field()
    superficieCubierta = scrapy.Field()

    
