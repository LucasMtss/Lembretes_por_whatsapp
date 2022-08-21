from db import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30), nullable=False, unique=True)

    def toJson(self):
        return {
            "id": self.id,
            "user": self.user,
        }

def searchAllUsers():
  users = Usuario.query.all()
  usersJson = [user.toJson() for user in users]
  return usersJson

def searchUser(user):
  userFound = Usuario.query.filter_by(user=user).first()
  if userFound is not None:
    return userFound.toJson()
  else:
    return None
    

def createUser(user):
  try:
      newUser = Usuario(user=user)
      db.session.add(newUser)
      db.session.commit()
  except Exception as error:
      print('ERROR CREATE USER', error)

def saveUser(user):
  registeredUser = searchUser(user)
  if registeredUser is None:
    createUser(user)