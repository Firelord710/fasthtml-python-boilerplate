from fasthtml.common import *
from shad4fast import *
from fasthtml.svg import Rect, Polyline, Path, Circle, Line
from starlette.staticfiles import StaticFiles
import os

app, rt = fast_app(
    pico=False,
    hdrs=(
        ShadHead(tw_cdn=True, theme_handle=True),
        Link(rel="stylesheet", href="/static/globals.css"),
    ),
)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Custom UI components
def CustomButton(*children, **kwargs):
    base_class = "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
    custom_class = kwargs.pop('classname', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return A(*children, **kwargs, classname=combined_class)


def CustomAvatar(**kwargs):
    return Div(classname="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full")(
        Img(src=kwargs.get('src', ''), classname="aspect-square h-full w-full"),
        Div(kwargs.get('fallback', ''),
            classname="flex h-full w-full items-center justify-center rounded-full bg-muted")
    )


def CustomInput(**kwargs):
    base_class = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    custom_class = kwargs.pop('classname', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return Input(**kwargs, classname=combined_class)


def CustomTextarea(**kwargs):
    base_class = "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    custom_class = kwargs.pop('classname', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return Textarea(**kwargs, classname=combined_class)


@rt("/")
def get():
    return Div(classname='flex min-h-[100dvh] flex-col')(
        Header(classname='sticky top-0 z-50 bg-[#1f0122] py-4 md:py-6')(
            Div(classname='container mx-auto flex items-center justify-between px-4 md:px-6')(
                A(href='#', classname='flex items-center', prefetch='{false}')(
                    MountainIcon(classname='h-8 w-8 text-[#f3f3f3]'),
                    Span('Obsidian Labs', classname='ml-2 text-lg font-bold text-[#f3f3f3]')
                ),
                Nav(classname='hidden md:flex items-center space-x-6')(
                    A('Services', href='#', classname='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}'),
                    A('Testimonials', href='#', classname='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}'),
                    A('Contact', href='#', classname='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}')
                ),
                Div(classname='md:hidden')(
                    CustomButton(
                        MenuIcon(classname='h-6 w-6 text-[#f3f3f3]'),
                        Span('Toggle navigation', classname='sr-only'),
                        classname='variant-ghost size-icon'
                    )
                )
            )
        ),
        Section(classname='bg-[#1f0122] py-20 md:py-32 relative')(
            Div(classname="absolute inset-0 bg-[url('/static/obsidian-texture.jpg')] bg-cover bg-center opacity-10"),
            Div(classname='container mx-auto px-4 md:px-6 relative z-10')(
                Div(classname='mx-auto max-w-3xl text-center')(
                    H1('Obsidian Labs', classname='text-4xl font-bold text-[#f3f3f3] md:text-5xl lg:text-6xl'),
                    P('Unlock the power of your data with our expert consulting and development services.',
                      classname='mt-4 text-xl text-[#d3d3d3] md:text-2xl'),
                    Div(classname='mt-8')(
                        CustomButton('Get Started',
                                     href='#',
                                     classname='inline-flex items-center rounded-md bg-[#f3f3f3] px-6 py-3 text-sm font-medium text-[#1f0122] transition-colors hover:bg-[#f3f3f3]/90 focus:outline-none focus:ring-2 focus:ring-[#1f0122] focus:ring-offset-2')
                    )
                )
            )
        ),
        Section(classname='py-16 md:py-24')(
            Div(classname='container mx-auto px-4 md:px-6')(
                Div(classname='mx-auto max-w-3xl text-center')(
                    H2('Our Services', classname='text-3xl font-bold text-foreground md:text-4xl'),
                    P('Obsidian Labs offers a wide range of data analytics and development services to help your business thrive.',
                      classname='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(classname='mt-10 grid grid-cols-1 gap-8 md:grid-cols-4')(
                    Div(classname='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        InfoIcon(classname='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Data Analytics', classname='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Leverage our expertise in data analysis to uncover valuable insights and drive informed decision-making.',
                          classname='mt-2 text-[#d3d3d3]')
                    ),
                    Div(classname='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        CodeIcon(classname='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Custom Development', classname='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Our skilled developers create tailored software solutions to meet your unique business needs.',
                          classname='mt-2 text-[#d3d3d3]')
                    ),
                    Div(classname='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        ConciergeBellIcon(classname='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Consulting', classname='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Our experienced consultants provide strategic guidance to optimize your data and technology infrastructure.',
                          classname='mt-2 text-[#d3d3d3]')
                    ),
                    Div(classname='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        BotIcon(classname='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Automation', classname='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Streamline your workflows and boost productivity with our custom automation solutions.',
                          classname='mt-2 text-[#d3d3d3]')
                    )
                )
            )
        ),
        Section(classname='bg-[#1a1a1a] py-16 md:py-24')(
            Div(classname='container mx-auto px-4 md:px-6')(
                Div(classname='mx-auto max-w-3xl text-center')(
                    H2('What Our Clients Say', classname='text-3xl font-bold text-foreground md:text-4xl'),
                    P("Hear from the businesses we've helped transform with our data analytics and development solutions.",
                      classname='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(classname='mt-10 grid grid-cols-1 gap-8 md:grid-cols-2')(
                    Div(classname='rounded-lg bg-[#1f0122] p-6 shadow-md')(
                        Blockquote(
                            '"Obsidian Labs has been an invaluable partner in our data transformation journey. Their expertise and attention to detail have been instrumental in unlocking new insights and driving our business forward."',
                            classname='text-lg font-medium leading-relaxed text-[#f3f3f3]'),
                        Div(classname='mt-4 flex items-center')(
                            CustomAvatar(src='/static/placeholder-user.jpg', fallback='JD'),
                            Div(classname='ml-4')(
                                Div('John Doe', classname='text-base font-semibold text-[#f3f3f3]'),
                                Div('CEO, Acme Corporation', classname='text-sm text-[#d3d3d3]')
                            )
                        )
                    ),
                    Div(classname='rounded-lg bg-[#1f0122] p-6 shadow-md')(
                        Blockquote(
                            '"Obsidian Labs has been a true partner in our data analytics journey. Their team\'s deep expertise and innovative approach have helped us uncover valuable insights and drive transformative change within our organization."',
                            classname='text-lg font-medium leading-relaxed text-[#f3f3f3]'),
                        Div(classname='mt-4 flex items-center')(
                            CustomAvatar(src='/static/placeholder-user.jpg', fallback='JA'),
                            Div(classname='ml-4')(
                                Div('Jane Appleseed', classname='text-base font-semibold text-[#f3f3f3]'),
                                Div('CTO, Acme Corporation', classname='text-sm text-[#d3d3d3]')
                            )
                        )
                    )
                )
            )
        ),
        Section(classname='py-16 md:py-24')(
            Div(classname='container mx-auto px-4 md:px-6')(
                Div(classname='mx-auto max-w-3xl text-center')(
                    H2('Get in Touch', classname='text-3xl font-bold text-foreground md:text-4xl'),
                    P("Have a project in mind? Let's discuss how Obsidian Labs can help.",
                      classname='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(classname='mt-10')(
                    Form(classname='mx-auto max-w-md space-y-4')(
                        Div(classname='flex flex-col items-center')(
                            Div(classname='w-full')(
                                Label('Name', htmlfor='name',
                                      classname='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomInput(id='name', type='text', required='',
                                            classname='bg-background text-foreground')
                            ),
                            Div(classname='w-full')(
                                Label('Email', htmlfor='email',
                                      classname='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomInput(id='email', type='email', required='',
                                            classname='bg-background text-foreground')
                            ),
                            Div(classname='w-full')(
                                Label('Message', htmlfor='message',
                                      classname='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomTextarea(id='message', required='',
                                               classname='bg-background text-foreground min-h-[150px]')
                            )
                        ),
                        CustomButton('Submit',
                                     classname='w-full bg-primary text-primary-foreground hover:bg-primary/90')
                    )
                )
            )
        )
    )


# SVG Icon components
def BotIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Path(d="M12 8V4H8"),
        Rect(width="16", height="12", x="4", y="8", rx="2"),
        Path(d="M2 14h2"),
        Path(d="M20 14h2"),
        Path(d="M15 13v2"),
        Path(d="M9 13v2")
    )


def CodeIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Polyline(points="16 18 22 12 16 6"),
        Polyline(points="8 6 2 12 8 18")
    )


def ConciergeBellIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Path(d="M3 20a1 1 0 0 1-1-1v-1a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v1a1 1 0 0 1-1 1Z"),
        Path(d="M20 16a8 8 0 1 0-16 0"),
        Path(d="M12 4v4"),
        Path(d="M10 4h4")
    )


def InfoIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Circle(cx="12", cy="12", r="10"),
        Path(d="M12 16v-4"),
        Path(d="M12 8h.01")
    )


def MenuIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Line(x1="4", x2="20", y1="12", y2="12"),
        Line(x1="4", x2="20", y1="6", y2="6"),
        Line(x1="4", x2="20", y1="18", y2="18")
    )


def MountainIcon(**props):
    return Svg(**props, xmlns="http://www.w3.org/2000/svg", width="24", height="24", viewbox="0 0 24 24", fill="none",
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round")(
        Path(d="m8 3 4 8 5-5 5 15H2L8 3z")
    )


print("Current working directory:", os.getcwd())
print("Static file path:", os.path.join(os.getcwd(), "static", "globals.css"))

serve()
