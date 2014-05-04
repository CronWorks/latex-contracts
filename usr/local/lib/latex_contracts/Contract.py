#!/usr/bin/env python

# Copyright 2012, 2013 J. Luke Scott
# This file is part of latex-contracts.

# latex-contracts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# latex-contracts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with latex-contracts.  If not, see <http://www.gnu.org/licenses/>.


from latex_python.JinjaBase import Date, JinjaTexDocument, JsonSerializable, escapeTex
from os import symlink, unlink
from os.path import dirname
from collections import OrderedDict

class Contract(JinjaTexDocument):
    def __init__(self, searchPath=None, signatureFilePath=None, **kwargs):
        self.title = 'Contract Agreement'
        self.subtitle = "This document is a Contractual Agreement (``Agreement'') between the parties listed."
        self.agreementDate = Date()
        self.showInitialsBox = True
        self.signSections = []
        self.clauses = OrderedDict() # format: {'sectionName': [clause list], ...}
    
        super(Contract, self).__init__(searchPath or dirname(__file__), **kwargs)
        
        self.signatureFilePath = signatureFilePath or dirname(__file__)

    def generate(self, outputFilename, system, variables={}):
        variables['contract'] = self

        # softlink to the signature files if necessary
        texFileDir = dirname(outputFilename)
        if self.needToSymlinkSignatureDirs(texFileDir):
            self.symlink('%s/initials' % self.signatureFilePath, '%s/initials' % texFileDir)
            self.symlink('%s/signatures' % self.signatureFilePath, '%s/signatures' % texFileDir)

        errors = super(Contract, self).generate(outputFilename, system, variables)
        if errors[0] or errors[1]:
            raise Exception("Errors: %s, Warnings: %s" % (errors[0], errors[1]))

        # remove softlinks to the signature files if necessary
        if self.needToSymlinkSignatureDirs(texFileDir):
            self.remove(texFileDir + '/signatures')
            self.remove(texFileDir + '/initials')


    def needToSymlinkSignatureDirs(self, texFileDir):
        return self.signatureFilePath and self.signatureFilePath != texFileDir

    def symlink(self, source, dest):
        try:
            symlink(source, dest)
        except:
            # file exists
            pass

    def remove(self, fileName):
        try:
            unlink(fileName)
        except:
            # file doesn't exist
            pass

    def addClause(self, sectionName, labelOrClauseObject, textOrNone = None):
        if isinstance(labelOrClauseObject, Clause):
            clause = labelOrClauseObject
        else:
            clause = Clause(label=labelOrClauseObject, text=textOrNone)
        if not sectionName in self.clauses:
            self.clauses[sectionName] = OrderedDict()
        self.clauses[sectionName][clause.label] = clause

    def getClauses(self, sectionName):
        try:
            result = '\n'.join(clause.__str__() for clause in self.clauses[sectionName].values())
            return result
        except:
            return ''

    def getInitialsFooterLines(self, person):
        signatureContent = self.getSignatureContentIfNecessary(person,
                                                               '\\hspace{0.3cm}\\smash{\\includegraphics[width=1.3cm]{%s}}'
                                                               % person.getInitialsRelativePath())
        dateContent = self.getSignatureContentIfNecessary(person,
                                                          '\\raisebox{3pt}{%s}'
                                                          % Date())
        result = '''
            \\vspace{7pt}\\small {%s} %s
            \\makebox[\\initialsSpaceWidth]{\\hrulefill}
            \\small Date %s
            \\makebox[\initialsSpaceWidth]{\hrulefill}%%
        ''' % (escapeTex(person), signatureContent, dateContent)
        return result

    def getNumberOfFooterRows(self):
        return 3  # by default, just 'initials:', 'page x of y', and 1 row of form lines

    def getSignatureFormlines(self):
        'Generate form lines for all FULL signatures (not getInitialsFooterLines) on the lease'
        result = []
        for person in self.getSigningPeople():
            signatureImage = self.getSignatureContentIfNecessary(person,
                                                                 '\\raisebox{-15pt}{\\smash{\\includegraphics[height=50pt]{%s}}}'
                                                                 % person.getSignatureRelativePath())
            signatureDate = self.getSignatureContentIfNecessary(person,
                                                                '\\raisebox{3pt}{%s}'
                                                                % Date())
            result.append('\\formLine[%s]{%s~- Signature}' % (signatureImage, escapeTex(person)))
            result.append('\\formLine[%s]{%s~- Date}' % (signatureDate, escapeTex(person)))
        return '\n'.join(result)

    # override this in subclasses
    def getSigningPeople(self):
        return[]

    def applySignedSections(self):
        result = ['\\providebool{signSection%d}\\booltrue{signSection%d}%%' % (sectionNumber, sectionNumber)
                  for sectionNumber
                  in self.signSections
                  ]
        return '\n'.join(result)

    # check whether we should print the signature in this section, and do it.
    def getSignatureContentIfNecessary(self, person, content):
        if not person.signatureFilename:
            return ''
        result = '\\ifbool{signSection\\arabic{section}}{\\rlap{%s}}{}' % content
        return result

    def formLineMulti(self, numberOfLines, label, filledInValue=''):
        formUnderlines = ['\\hrulefill%%\n'] * numberOfLines
        formUnderlines = '\\par\\vspace{\\formLineVerticalPadding}%%\n'.join(formUnderlines)
        result = '\\formLineWithContent{%s}{%s}{%s}' % (formUnderlines, filledInValue, label)
        return result

class Clause(JsonSerializable):

    def __init__(self, **kwargs):
        self.label = ''
        super(Clause, self).__init__(**kwargs)
        self._required = ['text']

    def __str__(self, *args, **kwargs):
        result = '\\clause[%s]{%s}' % (self.label, self.text.strip())
        return result

class Definition(JsonSerializable):
    # TODO
    pass

class Person(JsonSerializable):

    def __init__(self, **kwargs):
        # the filename of BOTH the signature AND the getInitialsFooterLines.
        # Signatures go in signatures/<filename>
        # Initials go in getInitialsFooterLines/<filename>
        # no checks are done whether the file actually exists - missing files flow through to TeX.
        # setting this implies that you want them to sign!! (assuming section is set through signSection(x))
        self.signatureFilename = None

        super(Person, self).__init__(**kwargs)

        self._required = ['name']

    def getInitialsRelativePath(self):
        if not self.signatureFilename:
            return ''
        result = 'initials/%s' % self.signatureFilename
        return result

    def getSignatureRelativePath(self):
        if not self.signatureFilename:
            return ''
        result = 'signatures/%s' % self.signatureFilename
        return result

    def getFullAddress(self):
        result = '''%s\\\\
                    %s''' % (getattr(self, 'address', ''),
                             self.getCityStateZip())
        return result

    def getCityStateZip(self):
        result = []
        for field in ['city', 'state', 'zip', 'country']:
            attr = getattr(self, field, None)
            if attr:
                result.append(attr)
        return ', '.join(result)

    def __str__(self, *args, **kwargs):
        return self.name

def buildContract(typeOrInstance, **kwargs):
    if isinstance(typeOrInstance, Contract):
        contract = typeOrInstance
    else:
        contract = typeOrInstance(**kwargs)
    
    # shorthand state & functions for building clauses/definitions    
    currentSection = None
    def section(label):
        currentSection = label
    def definition(term, meaning):
        contract.addDefinition(currentSection, term, meaning)
    def clause(heading, text):
        contract.addClause(currentSection, heading, text)
    
    return (contract, section, definition, clause)
