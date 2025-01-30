from setuptools import setup, find_packages

setup(
    name='django-tgauth',
    version='0.1.4',
    packages=find_packages(include=['auth_tg', 'auth_tg.*']),
    include_package_data=True,
    package_data={
        'auth_tg': [
            'management/commands/*.py',
            'static/auth_tg/js/*.js',
            'templates/admin/*.html',
            'templates/auth_tg/*.html',
            'migrations/*.py'
        ],
    },
    license='MIT',
    description='App for Django and DRF which give an opportunity to login via TG.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hraon88/tgauth',
    author='hraon88',
    author_email='irm7700@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=5.1.5,<5.2',
        'djangorestframework>=3.15.2',
        'pyTelegramBotAPI>=4.26.0',
        'requests>=2.25.0',
    ],
    python_requires='>=3.12',
)