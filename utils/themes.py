import os
def get_available_themes():
    '''
    get the available themes in template dir
    '''
    import settings
    TEMPLATE_DIRS = getattr(settings,'TEMPLATE_DIRS','')
    themes = []
    if TEMPLATE_DIRS:        
        if isinstance(TEMPLATE_DIRS,str):
            TEMPLATE_DIRS = (TEMPLATE_DIRS,)
        for template in TEMPLATE_DIRS:
            template = os.path.join(template,'themes')
            if os.path.isdir(template):                
                dirs = os.listdir(template)
                for d in dirs:                                       
                    if os.path.isdir(os.path.join(template,d)):                        
                        themes.append(d)    
    return themes