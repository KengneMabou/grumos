# coding: utf-8 
'''
Created on 4 août 2016

@author: kengne
'''
        
class UserMgtLogic:
    
    
    user = None
    

    def delete_user(self, id_user):
        from src.business.system.utilisateur import User
        
        error = None
        user = User.objects(id=id_user).first()
        
        if user :
            user.delete()
        
        return error
    

    def get_user(self, id_user):
        from src.business.system.utilisateur import User
        
        user = User.objects(id=id_user).first()
        
        return user
          
    def list_users(self):
        from src.business.system.utilisateur import User
        
        users = User.objects.all()
        
        return users


    def update_user(self, id_user, name, surname, email, login, password, passwordBis,  profile):
        """
            Methode pour la mise à jour d'un utilisateur
        """
        from src.business.system.utilisateur import User
        
       
        error = self.validate_form_update(id_user, name, surname, email, login, password, passwordBis, profile)
        user =  User.objects(id=id_user).first()
        
        if not error:
            user.name = name
            user.surname = surname
            user.email = email
            user.login = login
            if user.password != password:
                user.password = password
            else:
                User.call_hash = False
            user.profile = profile
            user.save()
        return error
    
    def update_user_profile(self, id_user, name, surname, email, login, password, passwordBis, profile=None):
        """
            Methode pour la mise à jour d'un utilisateur
        """
        from src.business.system.utilisateur import User
        
       
        error = self.validate_form_update(id_user, name, surname, email, login, password, passwordBis,profile)
        user =  User.objects(id=id_user).first()
        
        if not error:
            user.name = name
            user.surname = surname
            user.email = email
            user.login = login
            if user.password != password:
                user.password = password
            else:
                User.call_hash = False
            user.save()
        return error
    
    def create_user(self,_name, _surname, _email, _login, _password, _passwordBis, _profile):
        from src.business.system.utilisateur import User
        error = self.validate_form_create(_name, _surname, _email, _login, _password, _passwordBis, _profile)
        if not error:
            User(name = _name, surname = _surname, email=_email, login = _login, password = _password, profile = _profile).save()
        
        return error
        
    def validate_form_create(self, _name, _surname, _email, _login, _password, _passwordBis, _profile):
        
        """
        method for validatiing input data during user creation process
        TODO: Mettre en oeuvre un design pattern entre cette méthode et la méthode 'validate_form_create'. 
        Les 2 methodes ne varie que d'un simple test
        """
        from src.business.system.utilisateur import User
        
        error = None
    
        user_with_name = User.objects(login=_login).first()
        
        if user_with_name:
            if not error: 
                error = {}
            error["name_error"] = u"Ce login existe déjà"
            
        if _password == _passwordBis and _password == "":
            if not error: 
                error = {}
            error["empty_password_error"] = u"Le mot de passe ne peut être vide"
            
        if _password != _passwordBis:
            if not error: 
                error = {}
            error["password_not_matching_error"] = u"Les mots de passe ne correspondent"
            
            
        return error
    
    def validate_form_update(self, id_user, _name, _surname, _email, _login, _password, _passwordBis, _profile):
        
        """method for validatiing input data during user update process"""
        from src.business.system.utilisateur import User
        
        error = None
        
        user_with_name = User.objects(login=_login).first()
        
        if user_with_name and str(user_with_name.id) != str(id_user):
            if not error: 
                error = {}
            error["name_error"] = u"Ce Login existe déjà"
            
        if _password == _passwordBis and _password == "":
            if not error: 
                error = {}
            error["empty_password_error"] = u"Le mot de passe ne peut être vide"
            
        if _password != _passwordBis:
            if not error: 
                error = {}
            error["password_not_matching_error"] = u"Les mots de passe ne correspondent"
            
            
        return error
    
            
        
