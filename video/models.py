import ormar
from db.base import metadata, database




class MainMata(ormar.ModelMeta):
    metadata = metadata
    database = database



class Video(ormar.Model):
    class Meta(MainMata):
        pass

        tablename = "Video"



    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    file_text_ext: str = ormar.Text()





class Audio(ormar.Model):
    class Meta(MainMata):
        pass

        tablename = "Audio"



    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    file_text_ext: str = ormar.Text()





class VideoAudio(ormar.Model):
    class Meta(MainMata):
        pass

        tablename = "VideoAudio"



    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.String(max_length=500)
    file_audio_ext: str = ormar.String(max_length=1000)




class TextTransc(ormar.Model):
    class Meta(MainMata):
        pass

        tablename = "TextTransc"



    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    file_text_ext: str = ormar.Text()

