from celery import Celery

def make_celery(): 
    from . import app                                      
    celery = Celery(                                          
        'celery',                                     # for running in command line (???)
        backend=app.config['CELERY_RESULT_BACKEND'],  # celery output
        broker=app.config['CELERY_BROKER_URL'],       # celery input
        include=['webapp.tasks']                      # registering tasks      
    )                                                         
                                                              
    class ContextTask(celery.Task):                           
        def __call__(self, *args, **kwargs):                  
            with app.app_context():                           
                return self.run(*args, **kwargs)  
              
    celery.Task = ContextTask     
                                                              
    return celery                                           
    #> celery -A webapp.celery worker --loglevel=info                      
                                                            
celery = make_celery()
                             