#!/usr/bin/env python
# -*- coding: utf-8 -*-
from html import escape
import subprocess
import os

problemas_dir = "Problemas"
biblioteca_dir = "Biblioteca"

def get_sections(tipo):
    sections = []
    for diretorio in os.listdir(tipo):
        if not os.path.isfile(tipo+'/'+diretorio):
            subsections = []
            for arq in os.listdir(tipo+'/'+diretorio):
                if os.path.isfile(tipo+'/'+diretorio+'/'+arq):
                    nome = arq
                    subsections.append((nome, nome.split(".")[0]))
            sections.append((diretorio, subsections))
    return sections

def get_style(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['c', 'cc', 'cpp']:
        return 'cpp'
    elif ext in ['java']:
        return 'java'
    elif ext in ['py']:
        return 'py'
    else:
        return 'txt'

def get_tex(sections, tipo):
    tex = ''
    for (section_name, subsections) in sections:
        tex += '\\section{%s}\n' % section_name.split("&")[-1].replace("_", " ")
        for (filename, subsection_name) in subsections:
            tex += '\\subsection{%s}\n' % subsection_name.split("&")[-1].replace("_", " ")
            tex += '\\raggedbottom\\lstinputlisting[style=%s]{%s/%s}\n' % (get_style(filename), tipo+'/'+section_name, filename)
            #tex += '\\hrulefill\n'
            tex += '\\clearpage\n'
        tex += '\\clearpage\n'
    return tex

def get_html(sections, base):
    html = """
    <script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
    <style>
        * {
            font-family: Segoe UI, sans-serif;
        }

        .prettyprint span {
            font-family: Consolas, monospace;
        }

        ol { 
            padding: 0;
            list-style-type: none;
        }

        #index {
            font-size: 0.6rem;
        }

        #index li {
            cursor: pointer;
        }
    </style>
    """
    html += '<ol id="index">'
    for idx, (section_name, subsections) in enumerate(sections):
        html += '<h2><li>' + str(idx + 1) + '. ' + section_name.split("&")[-1] + '</li><ol></h2><ol>'
        for idx2, (filename, subsection_name) in enumerate(subsections):
            html += '<h3><li onClick="document.getElementById(\'' + filename.split("&")[-1] + '\').scrollIntoView()">' + str(idx + 1) + '.' + str(idx2 + 1) + '. ' + subsection_name.split("&")[-1] + '</li></h3>'
        html += '</ol>'
    html += '</ol>'

    html += '<ol>'
    for idx, (section_name, subsections) in enumerate(sections):
        html += '<h1><li>' + str(idx + 1) + '. ' + section_name.split("&")[-1] + '</li></h1>'
        html += '<ol>'
        for idx2, (filename, subsection_name) in enumerate(subsections):
            html += '<h2><li id="'+ filename.split("&")[-1] + '">' + str(idx + 1) + '.' + str(idx2 + 1) + '. ' + subsection_name.split("&")[-1] + '</li></h2>'
            html += '<pre class="prettyprint">'
            with open(base + '/' + section_name + '/' + filename, 'r') as f:
                html += escape(f.read())
            html += '</pre>'
        html += '</ol>'
    html += '</ol>'
    return html

def gera_html(tipo):
    sections = []
    if tipo == problemas_dir:
        sections = get_sections(tipo)
    else:
        sections = get_sections(tipo)

    html = get_html(sections, tipo)
    with open('index.html', 'w') as f:
        f.write(html)
    os.system('copy index.html /Y Documentos\\'+tipo+'.html')

def gera_pdf(tipo):
    sections = []
    if tipo == problemas_dir:
        sections = get_sections(tipo)
    else:
        sections = get_sections(tipo)

    # print(sections[0])
    # exit()
    tex = get_tex(sections, tipo)
    with open('contents.tex', 'w') as f:
        f.write(tex)
    latexmk_options = ["latexmk", "-pdf", "notebook.tex"]
    subprocess.call(latexmk_options)
    os.system('copy notebook.pdf /Y Documentos\\'+tipo+'.pdf')

def limpa():
    os.system('del /F notebook.aux')
    os.system('del /F notebook.fdb_latexmk')
    os.system('del /F notebook.fls')
    os.system('del /F notebook.out')
    os.system('del /F notebook.toc')
    os.system('del /F notebook.pdf')
    os.system('del /F notebook.log')
    os.system('del /F contents.tex')
    os.system('del /F index.html')

if __name__ == "__main__":
    limpa()
    gera_pdf(problemas_dir)
    gera_html(problemas_dir)
    limpa()
    gera_pdf(biblioteca_dir)
    gera_html(biblioteca_dir)
    limpa()


