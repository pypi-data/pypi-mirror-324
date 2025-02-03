from setuptools import setup, find_packages

setup(
        name='CoREMOF_tools',
        version='0.2.0',
        author='Guobin Zhao',
        author_email='sxmzhaogb@gmail.com',
        description='Python API for CoRE MOF 2024 DB',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/mtap-research/CoRE-MOF-Tools',
        packages=find_packages(),
        # package_data={
        # 'CoREMOF': [
        #     'data/*.json',
        #     'data/CSD/*.json',
        #     'data/SI/*.zip',
        #     'models/cp_app/ensemble_models_smallML_120_100/300/*',
        #     'models/cp_app/ensemble_models_smallML_120_100/350/*',
        #     'models/cp_app/ensemble_models_smallML_120_100/400/*',
        #     'models/stability/*'
        # ],
        # },
        install_requires=[
            'pymatgen',
            'ase',
            'juliacall',
            'molSimplify',
            'PACMAN-charge',
            'cloudpickle',
            'matminer',
            'xgboost',
            'scikit-learn==1.3.2',
            'mofchecker'
        ],
        extras_require={
            'zeopp': ['zeopp-lsmo']
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
        ],
        python_requires='>=3.9, <4',
        # entry_points={
        #     'console_scripts': [
        #         'coremof=CoREMOF:curate',
            # ],
        # },
    )
