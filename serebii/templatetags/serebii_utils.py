import bbcode
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def parse_bbcode(text):
    return mark_safe(bbcode.render_html(text))

@register.simple_tag(takes_context=True)
def voting_form_field_errors(context, award):
    errors = context['form'].errors.get('award_%s' % award.pk)
    if errors:
        return '<div class="alert alert-danger">%s</div>' % errors
    else:
        return ''

@register.simple_tag(takes_context=True)
def voting_form_field(context, award, nomination=None):
    return '<input type="radio" name="award_%s" value="%s"%s>' % (award.pk, nomination.pk if nomination else '', ' checked="checked"' if not nomination and not context['form']['award_%s' % award.pk].value() or nomination and str(context['form']['award_%s' % award.pk].value()) in (str(nom.pk) for nom in nomination.nominations) else '')

@register.simple_tag(takes_context=True)
def voting_form_errors(context):
    list_items = ['<dt><a href="#field-award_%s">%s</a></dt><dd>%s</dd>' % (context['form'].fields[field].award.pk, context['form'].fields[field].label, errors) for field, errors in context['form'].errors.items()]
    return '<dl class="errorlist">\n%s\n</dl>' % '\n'.join(list_items)