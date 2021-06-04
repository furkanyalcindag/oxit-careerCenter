from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def get_translation_word(which_lg, keyword):
    with open('example.json', 'r') as myfile:
        data = myfile.read()


def is_integer(param):
    try:
        x = int(param)
        return True
    except:
        return False



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)



    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8",'replace')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None