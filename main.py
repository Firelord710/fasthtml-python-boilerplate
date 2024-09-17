import os
from fasthtml.common import *
from shad4fast import *
from shad4fast import components as shad
from fasthtml.svg import Rect, Polyline, Path, Circle, Line
from starlette.staticfiles import StaticFiles
from dotenv import load_dotenv
import resend
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse

print("Current working directory:", os.getcwd())
print("Contents of .env file:")
try:
    with open('.env', 'r') as f:
        print(f.read())
except FileNotFoundError:
    print("File not found")

os.environ["RESEND_API_KEY"] = "re_hPjBZdRX_9ubXeGHBssdHzyLX5ipHUEGX"

# Attempt to load .env file, but don't fail if it's not present
load_dotenv(verbose=True)

# Use os.environ.get() with a default value
resend_api_key = os.environ.get("RESEND_API_KEY")
if not resend_api_key:
    raise ValueError("RESEND_API_KEY environment variable is not set")

resend.api_key = resend_api_key
print("Resend API key set")

app, rt = fast_app(
    pico=False,
    hdrs=(
        ShadHead(tw_cdn=True, theme_handle=True),
        Link(rel="stylesheet", href="/static/globals.css"),
    ),
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@rt("/submit-contact", methods=["GET", "POST"])
async def submit_contact(request: Request):
    if request.method == "POST":
        form = await request.form()
        name = form.get("name")
        email = form.get("email")
        message = form.get("message")

        if not all([name, email, message]):
            return JSONResponse({"success": False, "message": "All fields are required."})

        try:
            # Send email using Resend
            params = {
                "from": "Contact Form <contact@obsidian.bz>",
                "to": ["michael@obsidian.bz"],
                "subject": f"New Contact Form Submission from {name}",
                "html": f"""
                    <h1>New Contact Form Submission</h1>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                """
            }
            email_response = resend.Emails.send(params)
            print(email_response)

            return JSONResponse({"success": True, "message": "Your message has been sent successfully!"})
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return JSONResponse(
                {"success": False, "message": "An error occurred while sending your message. Please try again later."})

    # Handle GET request (e.g., redirect back to the main page)
    return RedirectResponse(url="/")


# Custom UI components
def CustomButton(*children, **kwargs):
    base_class = "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
    custom_class = kwargs.pop('cls', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return shad.Button(*children, **kwargs, cls=combined_class)


def CustomAvatar(**kwargs):
    return Div(cls="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full")(
        Img(src=kwargs.get('src', ''), cls="aspect-square h-full w-full"),
        Div(kwargs.get('fallback', ''),
            cls="flex h-full w-full items-center justify-center rounded-full bg-muted")
    )


def CustomInput(**kwargs):
    base_class = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    custom_class = kwargs.pop('cls', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return Input(**kwargs, cls=combined_class)


def CustomTextarea(**kwargs):
    base_class = "flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    custom_class = kwargs.pop('cls', '')
    combined_class = f"{base_class} {custom_class}".strip()
    return Textarea(**kwargs, cls=combined_class)


@rt("/")
def get():
    return Div(cls='flex min-h-[100dvh] flex-col')(
        Header(cls='sticky top-0 z-50 bg-[#1f0122] py-4 md:py-6')(
            Div(cls='container mx-auto flex items-center justify-between px-4 md:px-6')(
                A(href='#', cls='flex items-center', prefetch='{false}')(
                    MountainIcon(cls='h-8 w-8 text-[#f3f3f3]'),
                    Span('Obsidian Labs', cls='ml-2 text-lg font-bold text-[#f3f3f3]')
                ),
                Nav(cls='hidden md:flex items-center space-x-6')(
                    A('Services', href='#', cls='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}'),
                    A('Testimonials', href='#', cls='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}'),
                    A('Contact', href='#', cls='text-sm font-medium text-[#f3f3f3] hover:underline',
                      prefetch='{false}')
                ),
                Div(cls='md:hidden')(
                    CustomButton(
                        MenuIcon(cls='h-6 w-6 text-[#f3f3f3]'),
                        Span('Toggle navigation', cls='sr-only'),
                        cls='variant-ghost size-icon'
                    )
                )
            )
        ),
        Section(cls='bg-[#1f0122] py-20 md:py-32 relative')(
            Div(cls="absolute inset-0 bg-[url('/static/obsidian-texture.jpg')] bg-cover bg-center opacity-10"),
            Div(cls='container mx-auto px-4 md:px-6 relative z-10')(
                Div(cls='mx-auto max-w-3xl text-center')(
                    H1('Obsidian Labs', cls='text-4xl font-bold text-[#f3f3f3] md:text-5xl lg:text-6xl'),
                    P('Unlock the power of your data with our expert consulting and development services.',
                      cls='mt-4 text-xl text-[#d3d3d3] md:text-2xl'),
                    Div(cls='mt-8')(
                        CustomButton('Get Started',
                                     href='#',
                                     cls='inline-flex items-center rounded-md bg-[#f3f3f3] px-6 py-3 text-sm font-medium text-[#1f0122] transition-colors hover:bg-[#f3f3f3]/90 focus:outline-none focus:ring-2 focus:ring-[#1f0122] focus:ring-offset-2')
                    )
                )
            )
        ),
        Section(cls='py-16 md:py-24')(
            Div(cls='container mx-auto px-4 md:px-6')(
                Div(cls='mx-auto max-w-3xl text-center')(
                    H2('Our Services', cls='text-3xl font-bold text-foreground md:text-4xl'),
                    P('Obsidian Labs offers a wide range of data analytics and development services to help your business thrive.',
                      cls='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(cls='mt-10 grid grid-cols-1 gap-8 md:grid-cols-4')(
                    Div(cls='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        InfoIcon(cls='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Data Analytics', cls='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Leverage our expertise in data analysis to uncover valuable insights and drive informed decision-making.',
                          cls='mt-2 text-[#d3d3d3]')
                    ),
                    Div(cls='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        CodeIcon(cls='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Custom Development', cls='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Our skilled developers create tailored software solutions to meet your unique business needs.',
                          cls='mt-2 text-[#d3d3d3]')
                    ),
                    Div(cls='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        ConciergeBellIcon(cls='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Consulting', cls='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Our experienced consultants provide strategic guidance to optimize your data and technology infrastructure.',
                          cls='mt-2 text-[#d3d3d3]')
                    ),
                    Div(cls='rounded-lg bg-[#1f0122] p-6 text-center shadow-md transition-all hover:scale-105')(
                        BotIcon(cls='mx-auto h-12 w-12 text-[#f3f3f3]'),
                        H3('Automation', cls='mt-4 text-xl font-bold text-[#f3f3f3]'),
                        P('Streamline your workflows and boost productivity with our custom automation solutions.',
                          cls='mt-2 text-[#d3d3d3]')
                    )
                )
            )
        ),
        Section(cls='bg-[#1a1a1a] py-16 md:py-24')(
            Div(cls='container mx-auto px-4 md:px-6')(
                Div(cls='mx-auto max-w-3xl text-center')(
                    H2('What Our Clients Say', cls='text-3xl font-bold text-foreground md:text-4xl'),
                    P("Hear from the businesses we've helped transform with our data analytics and development solutions.",
                      cls='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(cls='mt-10 grid grid-cols-1 gap-8 md:grid-cols-2')(
                    Div(cls='rounded-lg bg-[#1f0122] p-6 shadow-md')(
                        Blockquote(
                            '"Obsidian Labs has been an invaluable partner in our data transformation journey. Their expertise and attention to detail have been instrumental in unlocking new insights and driving our business forward."',
                            cls='text-lg font-medium leading-relaxed text-[#f3f3f3]'),
                        Div(cls='mt-4 flex items-center')(
                            CustomAvatar(src='/static/placeholder-user.jpg', fallback='JD'),
                            Div(cls='ml-4')(
                                Div('John Doe', cls='text-base font-semibold text-[#f3f3f3]'),
                                Div('CEO, Acme Corporation', cls='text-sm text-[#d3d3d3]')
                            )
                        )
                    ),
                    Div(cls='rounded-lg bg-[#1f0122] p-6 shadow-md')(
                        Blockquote(
                            '"Obsidian Labs has been a true partner in our data analytics journey. Their team\'s deep expertise and innovative approach have helped us uncover valuable insights and drive transformative change within our organization."',
                            cls='text-lg font-medium leading-relaxed text-[#f3f3f3]'),
                        Div(cls='mt-4 flex items-center')(
                            CustomAvatar(src='/static/placeholder-user.jpg', fallback='JA'),
                            Div(cls='ml-4')(
                                Div('Jane Appleseed', cls='text-base font-semibold text-[#f3f3f3]'),
                                Div('CTO, Acme Corporation', cls='text-sm text-[#d3d3d3]')
                            )
                        )
                    )
                )
            )
        ),
        Section(cls='py-16 md:py-24')(
            Div(cls='container mx-auto px-4 md:px-6')(
                Div(cls='mx-auto max-w-3xl text-center')(
                    H2('Get in Touch', cls='text-3xl font-bold text-foreground md:text-4xl'),
                    P("Have a project in mind? Let's discuss how Obsidian Labs can help.",
                      cls='mt-4 text-muted-foreground md:text-xl')
                ),
                Div(cls='mt-10')(
                    Form(cls='mx-auto max-w-md space-y-4', id='contact-form', action='/submit-contact', method='POST')(
                        Div(cls='flex flex-col items-center')(
                            Div(cls='w-full')(
                                Label('Name', htmlfor='name',
                                      cls='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomInput(type='text', id='name', name='name', placeholder='Enter your name',
                                            required=True, cls='bg-background text-foreground')
                            ),
                            Div(cls='w-full')(
                                Label('Email', htmlfor='email',
                                      cls='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomInput(type='email', id='email', name='email', placeholder='Enter your email',
                                            required=True, cls='bg-background text-foreground')
                            ),
                            Div(cls='w-full')(
                                Label('Message', htmlfor='message',
                                      cls='text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70'),
                                CustomTextarea(id='message', name='message', placeholder='Enter your message',
                                               required=True, cls='bg-background text-foreground min-h-[150px]')
                            )
                        ),
                        CustomButton('Submit', type='submit', id='submit-button',
                                     cls='w-full bg-primary text-primary-foreground hover:bg-primary/90'),
                        Div(id='form-message', cls='mt-4 text-center')
                    )
                )
            )
        ),
        Script("""
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('contact-form');
            const submitButton = document.getElementById('submit-button');
            const formMessage = document.getElementById('form-message');

            form.addEventListener('submit', function(e) {
                e.preventDefault();
                submitButton.disabled = true;
                formMessage.textContent = 'Sending...';

                fetch(form.action, {
                    method: form.method,
                    body: new FormData(form),
                    headers: {
                        'Accept': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    formMessage.textContent = data.message;
                    if (data.success) {
                        form.reset();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    formMessage.textContent = 'An error occurred. Please try again later.';
                })
                .finally(() => {
                    submitButton.disabled = false;
                });
            });
        });
        """)
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
               stroke="currentColor", strokewidth="2", strokelinecap="round", strokelinejoin="round",
               preserveAspectRatio="xMidYMid meet")(
        Circle(cx="12", cy="12", r="10"),
        Line(x1="12", y1="16", x2="12", y2="12"),
        Circle(cx="12", cy="8", r="0.75", fill="currentColor", stroke="none")
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
