from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements

    """
    requirement_lst:List[str]= []
   
    try:

        with open('requirements.txt','r') as file:

            lines= file.readlines()
            for  line in lines:
                requirement=line.strip()
                if requirement and  requirement !='-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print(f"Error: The file requirements.txt was not found.")   

    return requirement_lst

print(get_requirements())

setup(
    name='Network_Security',
    version='0.0.1',
    author="Soham_Antre",
    author_email="sohamantre355@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)


            
