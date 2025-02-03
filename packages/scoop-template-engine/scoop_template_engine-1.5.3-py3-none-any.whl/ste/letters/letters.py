# This class introduces a parser object intended for templates of type letters.

# Resolve the dependencies.
import yaml

class parserObject(object):

    def __init__(self, parserInfo):
        # Initialize the data structure.
        self.latex = parserInfo.dataFileData.get("latex", {}) or {}
        self.letter = parserInfo.dataFileData.get("letter", {}) or {}
        self.outDirectory = parserInfo.outDirectory
        self.outFileBaseName = parserInfo.outFileBaseName
        self.templateBaseName = parserInfo.templateBaseName
        self.templateDescription = parserInfo.templateDescription
        self.scoopTemplateEngineVersion = parserInfo.scoopTemplateEngineVersion
        self.thisScriptAbsolutePathCallSummary = parserInfo.thisScriptAbsolutePathCallSummary
        self.dataFileData = parserInfo.dataFileData


    # LaTeXPrePreamble()
    # returns a string such as
    #   % Insert the user-defined prepreamble.
    #   \latex["prepreamble"] as is with "" as default.
    # It is intended to be included before \documentclass.
    def LaTeXPrePreamble(self):
        prePreambleString = """\
% Insert the user-defined prepreamble.
{prePreamble:s}\
    """.format(prePreamble = self.latex.get("prepreamble", "") or ""
            )
        return prePreambleString

    # LaTeXPreamble()
    # returns a string such as
    #   % Insert the user-defined preamble.
    #   \latex["preamble"] as is with "" as default
    # It is intended to be included after \documentclass.
    def LaTeXPreamble(self):
        preambleString = """\
% Insert the user-defined preamble.
{preamble:s}\
""".format(preamble = self.latex.get("preamble", "") or "",
            )
        return preambleString

    # LaTeXBibFiles()
    # returns latex["bibfiles"] as a list of strings
    # with "None"s eliminated.
    def LaTeXBibFiles(self):
        content = self.EnsureList(self.latex.get("bibfiles", "") or [])
        return [item for item in content if item]

    # LaTeXBody()
    # returns latex["body"] as a list of strings
    # with "None"s eliminated.
    def LaTeXBody(self):
        content = self.EnsureList(self.latex.get("body", "") or [])
        return [item for item in content if item]

    # DocumentClassOptions()
    # returns a comma separated string.
    # It is intended to be used as document class options in \documentclass.
    def DocumentClassOptions(self):
        content = self.EnsureList(self.latex.get("documentclassoptions", "") or [])
        return ",".join([item for item in content if item])

    # EnsureList(content)
    # returns content as is, if it already is a list, or [content] if not.
    def EnsureList(self, content):
        if isinstance(content, list):
            return content
        else:
            return [content]

    # CommandWrapper(content, command, separator)
    # where content is a string or a list of strings
    # and command is a string or a list of strings
    # returns a string such as
    #   \command{content}
    # .
    # When content == ["item1", "item2", "item3"] and
    # command == ["command1", "command2"],
    # then it returns
    #   \command1{item1}
    #   \command2{item2}
    #   \command2{item3}
    # .
    # The default separator, which is used to join the list items, is "\n".
    # When the separator is 'None', then no concatenation will be performed.
    def CommandWrapper(self, content, command, separator = "\n"):
        content = self.EnsureList(content)
        commands = self.EnsureList(command)
        commands = commands[:len(content)]  # truncate the commands list if necessary
        commands.extend(commands[-1:] * (len(content) - len(commands)))  # amend the commands list by repeating the last element if necessary
        commands = [command + "{" + item + "}" for (command, item) in zip(commands, content)]
        if separator is not None:
            return separator.join(commands)
        else:
            return commands

    # BibLaTeXResources()
    # returns a string such as
    #   \addbibresources{bibfile.bib}{}
    #   \addbibresources{bibfile.bib}{}
    # .
    def BibLaTeXResources(self):
        bibFiles = self.LaTeXBibFiles()
        return "\n".join([self.CommandWrapper(bibFile, "\\addbibresource") for bibFile in bibFiles])

    # BibLaTeXPrintBibliography()
    # returns a string such as
    #   \printbibliography
    def BibLaTeXPrintBibliography(self):
        return "\\printbibliography"

    # InputBody()
    # returns a string such as
    #   \input{file.tex}
    #   \input{file.tex}
    # .
    def InputBody(self):
        body = self.LaTeXBody()
        return "\n".join(["\\input{" + bodyFile + "}" for bodyFile in body])

    # Recipient()
    # returns the post scriptum string.
    def Recipient(self):
        return self.letter.get("recipient", "~") or "~"

    # CC()
    # returns a string such as
    #   \cc{Recipient \\ Recipient}
    # .
    def CC(self):
        content = self.letter.get("cc", "") or ""
        if content:
            return self.CommandWrapper("\\\\".join(self.EnsureList(content)), "\\cc")
        else:
            return content

    # Encl()
    # returns a string such as
    #   \encl{Document \\ Document}
    # .
    def Encl(self):
        content = self.letter.get("encl", "") or ""
        if content:
            return self.CommandWrapper("\\\\".join(self.EnsureList(content)), "\\encl")
        else:
            return content

    # PS()
    # returns the post scriptum string.
    def PS(self):
        return self.letter.get("ps", "") or ""

    # Subject()
    # returns the subject string.
    def Subject(self):
        return self.letter.get("subject", "") or ""

    # Date()
    # returns the date string.
    def Date(self):
        return self.letter.get("date", "") or ""

    # ScoopTemplateEngineSignature()
    # returns a signature containing the scoopTemplateEngineVersion.
    def ScoopTemplateEngineSignature(self):
        return "Created using the Scoop Template Engine version " + self.scoopTemplateEngineVersion + "."

    # TemplateTitle()
    # returns the template description as is.
    def TemplateTitle(self):
        return self.templateDescription

