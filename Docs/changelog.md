## Changelog 

3/2/2023

models.py: Added classes for platforms, vendors, and genres. The ManytoMany fields mean there can be multiple values attached to the game. Comments have been made to clarify on each class and their use.

admin.py: Added genre, platform, and seller

urls.py: New url to allow you to click a game in the list and see more details about it. 

views.py: New view to allow to look at each game individually upon clicking a link

game_list.html: Reformatted how it appears on the website. The title text is now a link you can click.

game_detail.html: Will hold additional information about the game such as all the vendors and maybe a summary. Currently still a work in progress.


2/23/2023

urls.py: Added support for About Us, Contact, and Catalog pages for the website

views.py: Used a generic listview for the catalog and added support for the other pages

models.py: Added new features. (Note: Still need to add image support)

Added templates to library folder and made their urls functional

The catalog page now shows results from our database


2/18/2023

Added migration folder (Needed to make updates to database)

Added models.py (Initialize the models and their parameters)

Added apps.py (Allows INSTALLED_APPS to use databases)

Added admin.py (Add models to see in admin mode)

Edited INSTALLED_APPS in settings.py to acknowledge database
