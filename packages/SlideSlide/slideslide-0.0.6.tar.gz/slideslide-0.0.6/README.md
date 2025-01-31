<h1 align="center">SlideSlide</h1>

<div align="center"><img width=500px src='https://raw.githubusercontent.com/Lakshit-Karsoliya/SlideSlide/refs/heads/main/assets/SLIDESLIDE.png'/></div>

<p align="center">SlideSlide Python Package</p>
<p align="center">
<a  href="https://github.com/Lakshit-Karsoliya/SlideSlide"><strong>Demo and Documentation Link</strong></a>
</p>

####  What's new in SlideSlide 0.0.6

* Added support for fonts (system installed)


##  What SlideSlide Does

This library convert JSON-structured content and transform it into visually appealing, well-formatted slides effortlessly

## The Problem SlideSlide Solves

This Python library bridges the gap between LLM-generated content and professional slide creation. While LLMs excel at generating text, their slide generation often lacks proper formatting and design. With this library, you can provide an LLM with JSON-structured content and transform it into visually appealing, well-formatted slides effortlessly.Built on top of the powerful **python-pptx** library, this tool ensures that your slides are polished and presentation-ready, saving you time and effort in designing slides from scratch 

## Why SlideSlide 

Sure, you could use python-pptx, but be ready to navigate its endless options and steep learning curve. As an AI engineer, I wanted results, not a tutorial. So, I built this library—simple, efficient, and to the point. Just one function, one JSON input, and boom—ready-to-go, beautifully formatted slides. No fuss, just slides that work.

<h2 align="center">Installation Instructions</h2>

```bash
pip install SlideSlide
```

<h2 align="center">Usage</h2>

```python
from SlideSlide.PresentationMaker import MakePresentation

data = [
    {
        "title":"Title of First Slide",
        "Content":"Content of First Slide"
    },
    {
        "title":"Title of First Slide and I am **BOLD** ",
        "Content":"Content of Second Slide"
    }
]

def MakePresentation(
        presentation_content=data,
        presentation_name="MyPresentation",
        add_ending_slide=True,
        template_name='SapphireBlue',
        template_mode='light',
        brand_name="SLIDESLIDE",
        verbose:bool=False
        ):

```



<h4 align='center'>Made with ❤️ by Lakshit</h4>