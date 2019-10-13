#!/bin/bash
action=$1
case "$action" in
	compile) 
		pybabel compile -d .
		;;
	update)
		pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot ../
		pybabel update -i messages.pot -d .
		;;
	*)
		echo "Usage: ./helper [update | compile]";
		;;	
esac

