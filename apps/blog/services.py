from django.http import HttpRequest


class BlogService:

    @staticmethod
    def slugify(string: str) -> str:
        """
        Creates slugs strings. Works fine with Farsi chars too.
        """
        return string.replace(' ', '-')
    
    @staticmethod
    def get_request_kwargs(request):
        """
        Extracts the parameters such as pk, slug etc.  
        (lookup_fields) from django HttpRequest object
        """
        return request.parser_context['kwargs']
