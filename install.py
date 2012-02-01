#!/usr/bin/python
from optparse import OptionParser
import os
import os.path
import sys
import shutil

desc = """Making $HOME a bit more like home."""
parser = OptionParser(epilog=desc)
parser.add_option('-b', '--backup', action='store_true', dest='backup',
									help="""make backups of current dotfiles (overrides '--overwrite')""")
parser.add_option('-o', '--overwrite', action='store_false', dest='backup',
									help="""overwrite current dotfiles (overrides '--backup')""")

home_dir =  os.getenv("HOME")
dotfiles_dir = home_dir + "/.dotfiles"
backup_dir = dotfiles_dir + "/backup"

def delete( file ):
	file = home_dir + "/." + file
	if os.path.exists( file ):
		if os.path.islink( file ):
			os.unlink( file )
		else:
			shutil.rmtree( file )


def link( file ):
	src = home_dir + "/." + file
	dst = dotfiles_dir + "/" + file
	os.symlink( dst, src )

def backup( file ):
	src = home_dir + "/." + file
	dst = backup_dir + "/" + file
	if os.path.exists ( src ):
		shutil.move( src, dst ) 

def prompt_backup():
	print( "Would you like to make a backup of files that will be overwritten?" )
	print( "Backups will be made in: " + backup_dir )
	while True:
		ans = raw_input("y/n/q(uit): ")
		first_char = ans[0].lower()
		if (first_char == 'q'):
			sys.exit( 0 )
		elif first_char == 'y':
			return True
		elif first_char == 'n':
			return False
		else:
			print( "Response unrecognized: " + ans )

def main():
	if not os.path.exists( dotfiles_dir ):
		error_msg = "Cannot install dotfiles: " + dotfiles_dir + " does not exist."
		print >> sys.stderr, error_msg
		sys.exit( 2 )

	(options, args) = parser.parse_args()
	if options.backup is None:
		options.backup = prompt_backup()
	
	if options.backup:
		if not os.path.exists( backup_dir ):
			os.makedirs( backup_dir )

	for file in os.listdir( dotfiles_dir ):
		if file in [ '.git', '.gitignore', 'install.py', 'bin', 'zsh', 'backup' ]:
			continue
		if options.backup:
			backup( file )
		else:
			delete( file )
		link( file )
		print "intstalled ~/." + file

if (__name__ == "__main__"):
	main()