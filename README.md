# serebii-fanfic-awards
The website for the Serebii.net forums fanfiction awards. This project is maintained by Dragonfree (antialiasis), but pull requests are welcome (so long as they're good pull requests).

This is a [Django](http://www.djangoproject.com) app. Refer to the Django documentation if you have no idea what is going on here.

The functionality is split across two 'apps', "awards" and "serebii". Roughly, serebii handles accounts and models that directly stand for forum entities, such as fics and members, whereas awards handles the actual awards part, but sometimes the distinction is a bit fuzzy. The level of documentation and comments varies; generally I comment things if I feel like I'm doing something nonobvious and forget about it otherwise. But if there's something that confuses you, just ask and I will try to explain it and document/comment it better.


## Installation

You *should* be able to run this on your own machine by following these instructions:

1. Make sure you have Python 2.7 and pip installed on your computer. I also highly recommend isolating your requirements in a [virtualenv](https://pypi.python.org/pypi/virtualenv).
2. Clone this repository.
3. (Optional but recommended) Navigate to the repository root folder, create a virtualenv (`virtualenv venv` will do it, if you have virtualenv installed) and activate it (`source bin/activate` on POSIX systems, `venv/Scripts/activate` on Windows).
4. Run `pip install -r local-requirements.txt` in the root of the repo. This will install Django and a couple of other Python packages. (The regular `requirements.txt` is used for the production setup on Heroku and requires some extra things that you won't need to set this up locally.)
5. Run `python manage.py migrate`. This should create all the necessary database tables.
6. Run `python manage.py createsuperuser` to create a superuser account for the admin. (This will ask you for an e-mail address, but only because Django does that by default; the awards site does not send any e-mails. You can leave it blank.)
7. You will have to configure a few settings. You can do this either by setting environment variables or creating a `local_settings.py` file that defines them as module-level variables. It is probably easiest for a local installation to use a `local_settings.py` file; you should create this file under the `sppfawards` folder. It does not need to contain anything other than the relevant variable definitions. The settings you almost definitely need are:
  - `PHASE`: Indicates the current phase of the awards. This can be set as `None` (when the awards have not yet started), `'nomination'` (in the nomination phase), `'voting'` (in the voting phase), or `'finished'` (when the awards are over). Changing this is how you can tinker with functionality from different phases.
  - `SEREBII_USER_ID` and `SEREBII_USER_PWHASH`: Forum credentials that the site will use to fetch threads/profiles. You should be able to get the appropriate values by inspecting your cookies for serebiiforums.com; these will be called `bb_userid` and `bb_password`. Without setting these, you're going to get errors when the site tries to fetch profiles, because guests can't view profiles. **Note that during the verification process, in order to verify as this account in the system, you will have to enter the URL to the "View your About Me as seen by everyone else" link at the top of the About Me tab in your profile (or simply add `&simple=1` at the end of the URL), not the regular profile URL.** This is because the site will see the forums as you see them, and your own profile has different HTML in order to allow you to edit it inline, which will confuse the site.
8. Run `python manage.py runserver`. If everything is right, this should start up the Django development server and you should be able to visit your local copy of the awards site in your web browser by navigating to `localhost:8000`. (You can also bind to a different port, e.g. `python manage.py runserver 8080` for port 8080.)

Some other settings you might want to set:
- `YEAR`: Defines what the site thinks is the current awards year. This defaults to 2015 (or, more specifically, to the `MAX_YEAR` setting).
- `DISCUSSION_THREAD`, `NOMINATION_THREAD`, `VOTING_THREAD` and `RESULTS_THREAD`: The URLs to the relevant forum threads, to be used whenever the site needs to link to them. These settings are blank by default, which is fine for testing, but it does mean these links will not work unless you set these settings.
- `SECRET_KEY`: By default, the secret key used to sign cookies, etc. is "insecure_default_key". That's okay when you're developing on your own machine, but if you're going to deploy this anywhere other people can get to it, you should probably set your `SECRET_KEY` to something actually secret that you make up.
- Also see [Django's settings documentation](https://docs.djangoproject.com/en/1.8/ref/settings/) if you want to, say, connect to a particular database (by default it creates a SQLite file in the root directory of the repository).

Note that you're going to need some actual awards in the database in order for the site to do much of anything. The repository includes a `data-dump.json` file that contains data about the awards and nominations from the 2013 awards, which I used for testing when developing the site; you should be able to load this data into the database with `python manage.py loaddata data-dump.json`. In order to work directly with these nominations you're going to have to set the `YEAR` setting to 2013. If you'd like to work with other years, or want to create awards and categories yourself for testing purposes, see the instructions under "The Admin" below.

Let me know if things explode catastrophically when you try to follow these instructions, and I will try to figure it out.


## The Admin

If you have set up a superuser as described in step six above, you should be able to go to `localhost:8000/admin` (or whatever port you're running it on) and log in as your superuser. This will get you into the Django admin interface, in which you can mess with most of the data in the system.

At the moment, the stuff you can mess with includes:

- **Groups**: This is a default Django thing and is not used in the awards system; ignore it.
- **Awards**: The actual awards people can be nominated for, like "Best Pokémon Chaptered Fic". On the list page, you can alter the display order of the awards; by clicking a name, you can edit its details or add one with the "Add Award" button in the top right corner.
- **Categories**: The award categories, like "Overall Fiction Awards" and "Reviewer Awards". These literally consist of a name. You can add/edit them in a similar way as awards.
- **Nominations**: The nominations for each award. It's easier to just add/edit these through the regular site interface, believe me. As an admin, you can edit a particular member's nominations by visiting `localhost:8000/nomination/[user-id]/`, where `[user-id]` is the Serebii user ID of that member. For example, if you wanted to edit my nominations, you could just go to `localhost:8000/nomination/388/`.
- **Year awards**: You're actually going to need this one. This basically defines which awards are active in a given year; for instance, the 2013 awards included the "Best Original Species" award, but it was removed for the 2014 awards because of the consistent lack of nominations for it. If you loaded the 2013 data, all you need to do to work with a different year is to go to the "Year awards" page and then use the little "Mass-edit awards for year" form in the top right corner next to the "Add year award" button to get a form for the year you want. On the resulting page, you can simply uncheck any categories you don't want for that year and then press the Save button at the bottom. Note that by default, it uses the previous year as a template if it has data for the previous year; thus, if you've loaded the 2013 data and then edit the year 2014, it'll start off with the same stuff checked as for 2013 and you can modify it from there. If you go straight to 2015, on the other hand, it'll have everything checked by default.
- **Fics**: Fanfics on Serebii. Each one has a title, one or more authors, a thread ID and (theoretically) a post ID. It is way easier to add fanfics using the public nomination interface than manually fiddling with IDs in here; you can add one simply by entering a URL and then clicking away from the box (provided you have Javascript enabled), even without saving your nominations. That interface does not at the moment support fics with post IDs, though, and if manual editing of a fic's data is needed (for instance, to add coauthors, which the system can't automatically detect), here's where you can do it.
- **Members**: Serebii forum members. They have a username and an ID. Again, it is far easier to add members through the public nomination interface.
- **Users**: Not to be confused with members, these are users of the Serebii fanfic awards site. Each user is optionally associated with a member (multiple users can be associated with the same member) and can be verified or unverified. You can verify an unverified user manually by clicking their username on the users page and checking the "Verified" box under "Member info". You can also give someone staff status, which means they can log into the admin and view things like voting stats.
