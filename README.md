### Test 1
I am testing, soon! 

This small helper has two funktions! scann al markdown files in folder and subfolders for latexCode and Forms like 
```
        r'\[ *(.*?) *\]',   # [ Formel ]
        r'\\\[(.*?)\\\]',   # \[ Formel \]
        r'\$\$(.*?)\$\$'    # $$ Formel $$
```

and creates an Assets Folder and stores wimages in high resolution in it.

you must start the workflow manually or use latex_to_image.yml_auto for automatic builds and after every pusch. its an bad idea! 

second. if Workflow ontime configurt you can use in the repo where this script runs 
 simple latex code between 

 ``` 
§§
\text{Komplexitätsindex} = \frac{\text{Systemkomplexität} \cdot \text{Variablen}}{\text{Verständlichkeit} + \text{Dokumentation}}
\
$$

 ``` 

# example output
$$
\text{Komplexitätsindex} = \frac{\text{Systemkomplexität} \cdot \text{Variablen}}{\text{Verständlichkeit} + \text{Dokumentation}}
\
$$



