from zope.interface import Interface, alsoProvides
from zope.component import adapts
from zope import schema
from plone.directives import dexterity
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFDefault.formlib.schema import ProxyFieldProperty

class IDexterityDublinCore(dexterity.Schema):
    """ Behavior interface to display Dublin Core metadata fields on Dexterity
        content edit forms.
        
        This schema duplicates the fields of zope.dublincore.IZopeDublinCore,
        in order to annotate them with Dexterity form hints and more helpful titles
        and descriptions.
    """

    # default fieldset
    title = schema.TextLine(
        title = u'Title',
        required = True
        )
    dexterity.order_before(title = '*')
        
    description = schema.Text(
        title = u'Summary',
        description = u'A short summary of the content.',
        required = False,
        )
    dexterity.order_before(description = '*')

    # categorization fieldset
    dexterity.fieldset(
        'categorization',
        label=u'Categorization',
        fields=['subjects', 'language'],
        )

    subjects = schema.Tuple(
        title = u'Categories',
        description = u'Also known as keywords, tags or labels, these help you categorize your content.',
        value_type = schema.TextLine(),
        required = False,
        )
    dexterity.widget(subjects = 'z3c.form.browser.textlines.TextLinesFieldWidget')

    language = schema.Choice(
        title = u'Language',
        vocabulary = 'plone.app.vocabularies.AvailableContentLanguages',
        required = False,
        )
        
    # dates fieldset
    dexterity.fieldset(
        'dates',
        label=u'Dates',
        fields=['effective', 'expires'],
        )
    
    effective = schema.Datetime(
        title = u'Publishing Date',
        description = u'If this date is in the future, the content will not show up in listings and searches until this date.',
        required = False
        )
    dexterity.widget(effective = 'collective.z3cform.datepicker.widget.DateTimePickerFieldWidget')
        
    expires = schema.Datetime(
        title = u'Expiration',
        description = u'When this date is reached, the content will nolonger be visible in listings and searches.',
        required = False
        )
    dexterity.widget(expires = 'collective.z3cform.datepicker.widget.DateTimePickerFieldWidget')

    # ownership fieldset
    dexterity.fieldset(
        'ownership',
        label=u'Ownership',
        fields=['creators', 'contributors', 'rights'],
        )

    creators = schema.Tuple(
        title = u'Creators',
        description = u'Persons responsible for creating the content of this item. Please enter a list of user names, one per line. The principal creator should come first.',
        value_type = schema.TextLine(),
        required = False,
        )
    dexterity.widget(creators = 'z3c.form.browser.textlines.TextLinesFieldWidget')

    contributors = schema.List(
        title = u'Contributors',
        description = u'The names of people that have contributed to this item. Each contributor should be on a separate line.',
        value_type = schema.TextLine(),
        required = False,
        )
    dexterity.widget(contributors = 'z3c.form.browser.textlines.TextLinesFieldWidget')
    
    rights = schema.Text(
        title=u'Rights',
        description=u'Copyright statement or other rights information on this item.',
        required = False,
        )

# Mark this interface as a form field provider
alsoProvides(IDexterityDublinCore, dexterity.IFormFieldProvider)

class DexterityDublinCore(object):
    """ This adapter uses ProxyFieldProperty to provide an implementation of IDexterityDublinCore
        that stores metadata directly on the object using the standard CMF DefaultDublinCoreImpl
        getters and setters.
    """
    adapts(IDexterityContent)
    
    def __init__(self, context):
        self.context = context
    
    title = ProxyFieldProperty(IDexterityDublinCore['title'], get_name = 'Title', set_name = 'setTitle')
    description = ProxyFieldProperty(IDexterityDublinCore['description'], get_name = 'Description', set_name = 'setDescription')
    subjects = ProxyFieldProperty(IDexterityDublinCore['subjects'], get_name = 'Subject', set_name = 'setSubject')
    language = ProxyFieldProperty(IDexterityDublinCore['language'], get_name = 'Language', set_name = 'setLanguage')
    effective = ProxyFieldProperty(IDexterityDublinCore['effective'], get_name = 'effective', set_name = 'setEffectiveDate')
    expires = ProxyFieldProperty(IDexterityDublinCore['expires'], get_name = 'expires', set_name = 'setExpirationDate')
    creators = ProxyFieldProperty(IDexterityDublinCore['creators'], get_name = 'listCreators', set_name = 'setCreators')
    contributors = ProxyFieldProperty(IDexterityDublinCore['contributors'], get_name = 'Contributors', set_name = 'setContributors')
    rights = ProxyFieldProperty(IDexterityDublinCore['rights'], get_name = 'Rights', set_name = 'setRights')
