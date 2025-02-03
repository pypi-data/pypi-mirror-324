![resumaker image](./extra/resumaker.png)


[![PyPI -
Version](https://img.shields.io/pypi/v/resumaker.svg)](https://pypi.org/project/resumaker)
[![PyPI - Python
Version](https://img.shields.io/pypi/pyversions/resumaker.svg)](https://pypi.org/project/resumaker)

-----
# Resumaker

Resumaker is a tool that creates ATS-friendly, professionally formatted,
multiple, and multi-targeted resumes from a single YAML file. Write down all the
details and let Resumaker handle the formatting and structuring.

Let's assume you know Python and JS, and you're applying to two different
companies for two different roles. You'll need to have a different resume for
each option. It can be counterproductive to manually write LaTeX code or use an
office suite like Word or LibreOffice Writer to write your resume. Instead,
write all the information in a YAML file, and Resumaker will create six resumes
for you, nicely formatted and ATS-friendly.

See [quickstart](#quickstart).

## Disclaimer

This is a pre-release version and the current template is intended for software
engineers and  has the following fields:

- Name, Location, Professional Summary, Education, Skills, Work Experience,
  Projects, and Links.

## Installation

Install `resumaker` with pip.

```console
pip install resumaker
```

### Requirements

- `pdflatex`

You also need the following TeX packages:

- `parskip`, `array`, `ifthen`, `graphicx`, `ebgaramond`, `hyperref`

For [Fedora](https://docs.fedoraproject.org/en-US/neurofedora/latex/), run:

```console
sudo dnf install texlive-scheme-medium texlive-parskip texlive-ebgaramond
```

For Ubuntu, read the
[gist](https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d).

If you face any package issues, please download the package for your system and
create a pull request to include the package name above. If you use another
distribution, please search with your package manager and consider contributing
by adding the package name to the list above.

## Quickstart

You need a YAML file to write the details. This file can be categorized into two
parts:

### Common Part

The fields are common to all resumes:

- name, location, contact, education, links

### Targeted Part

This will be different for each resume:

- summary, skills, work experience, projects

From the following `resume.yml`, two PDFs will be created: [testuser-swe.pdf](./extra/testuser-swe.pdf)
and [testuser-machine_learning.pdf](./extra/testuser-machine_learning.pdf) by running:

```shell
resumaker -f resume.yml
```

```yml
# common fields
name: Test User
location: Fake City, India 

contact:
  email: test.user@example.com 
  phone: +91 12345 67890 # make sure to include country code
  linkedin: sujaudd1n # only username
  github: sujaudd1n # only username

education:
  - name: XYZ University
    location: ABC City, India
    duration: 2010 - 2014
    degree: Bachelor of Technology in Computer Science
    achievements:
      - 'GPA: 3.5/10 (I was going for 9, but pizza happened)' # in '' because in yml you have to escape :
      - University Topper in going late
      - Published Research Paper which 12 people have read, including me

  - name: PQR Institute
    location: DEF City, India
    duration: 2014 - 2016
    degree: Master of Technology in Artificial Intelligence
    achievements:
      - Research Assistant
      - Filed Patent, Now I Just Need to Remember What It Was For

links:
  algorithms:
    - name: Leetcode
      url: https://leetcode.com/sujaudd1n
      url_text: leetcode.com/sujaudd1n
  open-source:
    - name: Github
      url: https://github.com/sujaudd1n
      url_text: github.com/sujaudd1n

swe:
  summary:
    title: Senior Software Engineer
    text: >
      Meet the software engineer who learned the value of TDD from a very special teacher:
      Murphy's Law. After a memorable SaaS meltdown in production, I learned to test before
      I deploy. Now, my code works, and my blood pressure thanks me.

  skills:
    languages: [Go, Come, Python, C++]
    libraries: [Jango, Reaction]
    databases: [OurSQL, PostgreSQL, MangoDB]
  
  work_experience:
    - company-name: ABC Corporation
      location: Fake City, India
      role: Software Engineer
      duration: 2016 - 2018
      contributions:
        - Developed a machine learning model for image classification for cat and not-cat
        - Improved search engine performance by 2.18\%
        - Collaborated on a new feature launch
    - company-name: DEF Startups
      location: ABC City, India
      role: Software Engineer
      duration: 2018 - 2020
      contributions:
        - Built a real-time analytics dashboard to watching numbers move in real-time
        - Enhanced payment gateway reliability from "it usually works" to "it almost always works"
        - Launched a new feature with the team in one night and most of tests failed in the morning

  projects:
    - name: Project Alpha
      techstack: [Python, Django, MySQL]
      details:
        - Developed a web application for e-commerce where you can buy things
        - Implemented a secure payment gateway...yes, your money is safe, ig
        - Deployed on a cloud platform aka rented computers

    - name: Project Beta
      techstack: [Java, Spring, MongoDB]
      details:
        - Created a mobile app for social media because the world needed another one, right?
        - Designed a functional chatbot 
        - Successfully deployed on a cloud platform 

machine_learning:
  summary:
    title: Senior Machine Learning Engineer
    text: Making computers solve complex problems, one model at a time. Currently, they're smarter than me, but that's not saying much.

  skills:
    languages: [Python, R, Julia, thinking about learning lisp to feel better]
    libraries: [TensorFlow, PyTorch, scikit-learn]
    databases: [MySQL, PostgreSQL, MongoDB]
  
  work_experience:
    - company-name: GHI Research
      role: Machine Learning Engineer
      duration: 2020 - 2022
      location: Fake City, India
      contributions:
        - Developed an NLP model with high accuracy
        - Launched a new product with the research team
        - Improved computer vision model performance, now it can see me coming... to the fridge

    - company-name: JKL Labs
      role: Machine Learning Engineer
      duration: 2018 - 2020
      location: ABC City, India
      contributions:
        - Built a recommender system with strong results
        - Successfully built something.
        - Enhanced some models, and now they perform their job better than before

  projects:
    - name: Project Gamma
      techstack: [Python, PyTorch, MongoDB]
      details:
        - Developed a time series forecasting model
        - Deployed on a cloud platform with high uptime
        - Achieved 90\% accuracy, on a good day, with the wind in my favor

    - name: Project Delta
      techstack: [R, TensorFlow, MySQL]
      details:
        - Created a clustering analysis model for categorizing my mental health.
        - Deployed on a cloud platform with good performance, no complaints so far
        - Reached 85\% accuracy, close enough, right? Right?!
# these are mostly fake data
```

Note: You need to escape `%`, `:`, `$` among other things as these have
special meaning in YAML, Tex.

## Configuration

Here is the text with corrected grammar:

This is a pre-release, so minimal configurations are provided.

Configs should be in a file called `config.yml` and it should be a dictionary.

Valid keys:

- `RESUME_FILENAME`: The default filename to look for if you run `resumaker`
  with no options.
- `ORDER`: The ordering of resume sections.

Sample config.yml:

```yml
RESUME_FILENAME: [my-resume.yml]
ORDER : [summary, skills, education, work_experience, projects, links]

```

## License

`resumaker` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
