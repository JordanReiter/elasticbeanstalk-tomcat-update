The file elasticbeanstalk_tomcat_update.py allows you to make modifications to
parts of the server.xml used by the Elastic Beanstalk Tomcat deployment without
actually having to supply your own server.xml file (and potentially overwriting
important or necessary changes to the file when your environment's platform is
updated).

In order to use this script, you'll need to add it to an existing or new
.ebextensions file (I've included a sample version that sets
tomcatAuthentication to false for the AJP connector).

The part you need to edit is the section marked CHANGES. You can make two kinds
of changes:

 - Add attributes to an element
 - Delete an element

For each change, you need to specify `path` (in XPath format) as well as the
target attributes (`target_attrs`) if you don't want to match all elements of
that type.

Then you specify the action either by including a value for `updated_attrs` or
by specifying `action` "DELETE" (must be uppercase) to indicate you want to
delete the target element.

The original version of the server.xml file will be saved as server.xml.orig if
you need to restore it, although note that if the script is run more than once
the original version will be overwritten.
