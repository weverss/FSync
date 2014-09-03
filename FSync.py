import os
import time
import shutil
import sublime
import sublime_plugin

#################################################################
# Classe / plugin para sicronização entre ambientes de trabalho #
#################################################################
class FSync( sublime_plugin.EventListener ) :

	# Ambiente de trabalho local
	local_workspace = "/home/wevers/workspace"

	# Ambiente de trabalho remoto
	remote_workspace = "/mnt/dev_desenvolvedores/51"

	# Última data de sincronização entre os ambiente
	last_sync_time = 0

	# Extensões ignoradas
	ignored_file_extensions = [ ".svn-base" , "wc.db" ]

	########################################################################
	# Método executado pelo Sublime, de maneira assícrona, a cada "Ctrl+S" #
	########################################################################
	def on_post_save_async( self , view ) :
		self.run_pre_sync()
		self.sync()

	############################################################
	# Atualiza data de sicronização no arquivo de configuração #
	############################################################
	def run_pre_sync( self ) :
		if os.path.isfile( self.remote_workspace + "/.folhasync" ) :
			# Obtém última data de sincronização.
			self.last_sync_time = time.gmtime(
				os.path.getmtime( self.remote_workspace + "/.folhasync" )
			)

		open( self.remote_workspace + "/.folhasync" , "w" ).close()

	########################
	# Sincroniza ambientes #
	########################
	def sync( self ) :
		changed_files = self.get_changed_files()

		if not changed_files :
			return
		
		print( "Sincronizando workspaces:" )
		for local_file in changed_files :
			
			remote_file_directory = local_file["directory_path"].replace(
				self.local_workspace ,
				self.remote_workspace
			)

			# Cria diretórios no ambiente remoto, caso não existam.
			if os.path.isdir( remote_file_directory ) == False :
				os.makedirs( remote_file_directory )
				
			# Sincroniza arquivos entre os ambientes.
			shutil.copy( local_file["file_path"] , remote_file_directory )
			print( "+ " + local_file["file_path"] )		
		print( "Sincronizado." )

	#############################################################
	# Retorna arquivos modificados deste a última sincronização #
	#############################################################
	def get_changed_files( self ) :
		changed_files = []

		for top , directories , files in os.walk( self.local_workspace ) :		
			for file in files :
				# Monta caminho para o arquivo.
				file_path = os.path.join( top , file )
				
				file_modification_time = time.gmtime(
					os.path.getmtime( file_path )
				)
				
				# Arquivos não modificados após última sincronização.
				if file_modification_time < self.last_sync_time :
					continue

				if self.ignore_file( file_path ) :
					continue

				changed_files.append( {
					"directory_path" : top ,
					"file_path" : file_path
				} )

		return changed_files

	#######################################################
	# Ignora sincronização de arquivo baseado na extensão #
	#######################################################
	def ignore_file( self , file_path ) :
		for ignored_file_extension in self.ignored_file_extensions :
			if file_path.endswith( ignored_file_extension ) :
				return True

		return False