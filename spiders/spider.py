# -*- coding: utf-8 -*-
# import sys
# reload(sys)
import scrapy
import re
import string
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrap_prueba.items import ScrapPruebaItem

class PruebaSpider(CrawlSpider):
	name = 'scrap_prueba'
	item_count = 0
	allowed_domain = ['www.zonaprop.com.ar']
	start_urls = ['https://www.zonaprop.com.ar/departamentos-venta-olivos-vicente-lopez-vicente-lopez-florida-la-lucila-vicente-lopez-munro-carapachay-florida-oeste-villa-adelina-vicente-lopez-2-ambientes-menos-160000-dolar.html']
	

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//*[@id="paginadoListado"]/div/ul/li[7]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h4[@class="aviso-data-title"]/a')),
			callback = 'parse_item', 
			follow = False)
	}

	def parse_item(self, response):

		regexAnunciante = re.compile(r'Código del anunciante: \b[\w.]+')
		regexZonaProp = re.compile(r'Código ZonaProp: \b[\w.]+')
		regexAntiguedad = re.compile(r'Publicado hace \b[\w.]+ días')
		regexPrecio = re.compile(r'U\$S [\d.]+')
		regexSuperficieTotal = re.compile(r'Superficie total')
		

		regexSuperficieCubierta = re.compile(r'Superficie cubierta')
		regexSuperficieCubierta2 = re.compile(r'Antigüedad: [\d]+  años')
		regexSuperficieCubierta3 = re.compile(r'Antigüedad: En construcción')

		zp_item=ScrapPruebaItem()

		#----descripcion
		zp_item['descripcion']=response.xpath('//span[@class="nombre"]/text()').extract_first()
		#zp_item['precio']=response.xpath('normalize-space(//*[@id="layout-content"]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/p/strong/text())').extract()
		
		#----Linea de codigo
		linea_codigo=response.xpath('//span[@class="valor"]/text()').extract()

		self.logger.info('\n--- PROPIEDAD ---')

		for campo_aux in linea_codigo:
			campo= campo_aux.encode("utf8")

			if regexAnunciante.search(campo):
				zp_item['codigoAnunciante']=self.extraeCodigoAnunciante(campo)
				self.logger.info('Campo: ' + campo)

			elif regexZonaProp.search(campo):
				zp_item['codigoZonaProp']=self.extraeCodigoZonaProp(campo)
				self.logger.info('Campo: ' + campo)

			elif regexAntiguedad.search(campo):
				zp_item['antiguedadAviso']=self.extraeAntiguedadAviso(campo)
				self.logger.info('Campo: ' + campo)

			elif regexPrecio.search(campo):
				zp_item['precio']=self.extraePrecio(campo)
				self.logger.info('Campo: ' + campo)

			#
		#else: self.logger.info('  --Es otro campo: ' + campo)
			
		#----direccion
		zp_item['direccion']= self.extraeDireccion(response.xpath('normalize-space(//div[contains(@class, "list list-directions")])').extract())

		#----Linea de datos
		linea_datos=response.xpath('//span[contains(@class, "nombre")]/text()').extract()
		for campo_aux_datos in linea_datos:
			campo_datos= campo_aux_datos.encode("utf8")
			
			if regexSuperficieTotal.search(campo_datos):
				zp_item['superficieTotal']=self.extraeSuperficieTotal(campo_datos_ant)
				self.logger.info('Campo Datos: ' + campo_datos_ant)

			#elif regexSuperficieCubierta.search(campo_datos):
			#	zp_item['superficieCubierta']=self.extraeSuperficieCubierta(campo_datos_ant)
			#	self.logger.info('Campo Datos anterio: ' + campo_datos_ant)

		#	else: self.logger.info('  --Es otro campo: ' + campo_datos)

			campo_datos_ant=campo_datos

		self.item_count += 1
		#print self.item_count
		#if self.item_count > 80:
		
		#	raise CloseSpider('item_exceeded')
		yield zp_item

	def extraePrecio(self, campoPrecio):
		# valor , codigo de anunciante, codigo zona prop, publicado hace.
		
		return campoPrecio.split(' ')[1]

	def extraeCodigoZonaProp(self, campoZonaProp):
		# valor , codigo de anunciante, codigo zona prop, publicado hace.
		#print "Linea codigo ZP:" + linea_codigo[2]
		return campoZonaProp.split(' ')[2]

	def extraeCodigoAnunciante(self, campoAnunciante):
		return campoAnunciante.split(' ')[3]

	def extraeDireccion(self, linea_direccion):
		#print "Linea codigo A:" + linea_codigo[1]
		return linea_direccion

	def extraeAntiguedadAviso(self, campoAntiguedad):
		return campoAntiguedad.split(' ')[2]

	def extraeSuperficieTotal(self, campoDatosSuperficieTotal):
		regexSuperficieTotal2 = re.compile(r'[\d]+')

		if regexSuperficieTotal2.match(campoDatosSuperficieTotal):
			return campoDatosSuperficieTotal
		return campoDatosSuperficieTotal.split(' ')[2]
		
	def extraeSuperficieCubierta(self, campoDatosSuperficieCubierta):
	#	if regexSuperficieCubierta2.search(campoDatosSuperficieCubierta):
	#		return campoDatosSuperficieCubierta.split(' ')[1]
		
		return 0



