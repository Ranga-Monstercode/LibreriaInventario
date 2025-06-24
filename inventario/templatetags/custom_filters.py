from django import template

register = template.Library()

@register.filter
def formatear_run(run):
    """
    Formatea un RUN chileno a formato xx.xxx.xxx-x
    """
    if not run:
        return ''
    
    run = run.replace(".", "").replace("-", "")
    cuerpo = run[:-1]
    dv = run[-1]

    cuerpo_con_puntos = "{:,}".format(int(cuerpo)).replace(",", ".")
    return f"{cuerpo_con_puntos}-{dv}"
