import appdirs
import os


def config():
    
    try:
        
        dir = appdirs.user_config_dir()
        
        config = f"{dir}/shodanx"
        
        if not os.path.exists(config):
            
            os.makedirs(config)
        
        return config
    
    except Exception as e:
        
        pass
