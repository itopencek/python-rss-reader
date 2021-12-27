from ArticleParserApp import db
from ArticleParserApp.database.models.exceptions.api import WrongParamException
from ArticleParserApp.database.models.models import Site


def get_site_from_name(name):
    """
    Finds Site by its name.
    :param name: name of site
    :return: Site object
    """
    site = Site.query.filter_by(name=name).first()
    if site is None:
        raise WrongParamException('name')

    return site


def add_site(site):
    """
    Adds site to database.
    :param site: dict of site
    """
    site_to_db = Site(name=site['name'], url=site['url'], description=site['description'])
    db.session.add(site_to_db)
    db.session.commit()


def remove_site_by_id(site_id):
    """
    Removes site from database.
    :param site_id: id of site
    """
    Site.query.filter_by(id=site_id).delete()
    db.session.commit()


def remove_site_by_name(name):
    """
    Removes site from database.
    :param name: name of site
    """
    Site.query.filter_by(name=name).delete()
    db.session.commit()


def get_all_sites():
    """
    Returns all sites from database.
    """
    return Site.query.all()
