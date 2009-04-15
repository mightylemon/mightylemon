#!/bin/sh
TEMP=tmp
mkdir -p $TEMP

cd $TEMP

# Download all the libraries
hg clone http://dev.pocoo.org/hg/pygments-main pygments
svn checkout http://django-gravatar.googlecode.com/svn/trunk/ django-gravatar-read-only  
wget "http://prdownloads.sourceforge.net/docutils/docutils-0.5.tar.gz?download"
tar -xvzf docutils-0.5.tar.gz
git clone git://gitorious.org/python-markdown/mainline.git
git clone git://github.com/jezdez/django-comment-utils.git
git clone git://github.com/leah/django-elsewhere.git
mv mainline markdown
svn co http://django-tagging.googlecode.com/svn/trunk/ django-tagging


for zipfile in "django-comment-utils comment_utils" "django-elsewhere elsewhere" "django-gravatar-read-only gravatar" "django-tagging tagging" "docutils-0.5 docutils" "markdown markdown" "pygments pygments"
do
  set -- $zipfile
  cd $1
  rm -f "$2.zip"
  zip $2 `find $2 -name .svn -prune -o -type f ! -name '*.pyc' ! -name '*.[pm]o' -print`
  mv $2.zip ../../
  cd ..
done

# Back to vendor
cd ../
