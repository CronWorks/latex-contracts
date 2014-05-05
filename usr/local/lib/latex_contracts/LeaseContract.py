# /usr/bin/env python

# Copyright 2012, 2013, 2014 J. Luke Scott
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


from latex_python.JinjaBase import JsonSerializable, Money, Percent
from Contract import Contract, Person, Address
from re import sub

class Lessor(Person):
    pass  # _required & __init__ are the same

class Tenant(Person):
    def __init__(self, **kwargs):
        self.forwardingAddress = Address()
        self.forwardingPhoneNumber = ''
        super(Tenant, self).__init__(**kwargs)

class Occupant(Person):
    pass # _required & __init__ are the same

PROPERTY_ELEMENTS = {'appliances': 'Appliances',
                     'cleanliness':'Cleanliness',
                     'closet': 'Closet Space',
                     'sink': 'Sink and Faucet',
                     'sinkWithInsert': 'Sink, Sink Insert, and Faucet',
                     'countertops': 'Counter tops',
                     'tileCountertops': 'Tile counter tops',
                     'cupboards':'Cupboards, Drawers',
                     'electrical': 'Lights, Outlets',
                     'electricMeter': 'Electric Meter Reading',
                     'furniture': 'Any furniture owned by Lessor',
                     'general': 'General condition/damage',
                     'gasMeter': 'Gas Meter Reading',
                     'heatingOil': 'Heating Oil Level',
                     'shower': 'Shower and Surround',
                     'smokeDetectors': 'List any inoperable smoke detectors',
                     'toilet': 'Toilet',
                     'walls': 'Walls, Floors, Windows, Blinds',
                     'washer': 'Washer/Dryer',
                     'waterMeter': 'Water Meter Reading',
                     }

class SubjectToInspection(JsonSerializable):
    def __init__(self, **kwargs):
        self._inspectionItems = []  # items to attach to the room (subclass as appropriate)
        self._moveInConditions = {}
        self._moveOutConditions = {}
        super(SubjectToInspection, self).__init__(**kwargs)

    def setCondition(self, itemId, moveInOrOut, condition):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        if not conditionDict:
            setattr(self, '_%sConditions' % moveInOrOut, conditionDict)
        conditionDict[itemId] = condition

    def getConditionsTuples(self, moveInOrOut):
        conditionDict = getattr(self, '_%sConditions' % moveInOrOut, {})
        resultDict = {}
        for itemId in sorted(self._inspectionItems):
            label = PROPERTY_ELEMENTS[itemId]
            condition = getattr(conditionDict, itemId, '')
            resultDict[label] = condition
        return [(label, resultDict[label]) for label in sorted(resultDict.keys())]

class Room(SubjectToInspection):
    def __init__(self, label=None, **kwargs):
        # shortcut instantiation syntax
        # if left empty, str(room) will return class name ('Bedroom')
        kwargs['label'] = label or ''
        super(Room, self).__init__(**kwargs)

    def __str__(self):
        # 'TheSpecialRoomClass' > 'The Special Room Class'
        roomType = sub(r'([A-Z])', r' \1', self.__class__.__name__).strip()
        return ('%s %s' % (self.label, roomType)).strip()

class Kitchen(Room):
    def __init__(self, label=None, tileCountertops=False, sinkWithInsert=False, **kwargs):
        super(Kitchen, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'sink',
                                 'countertops',
                                 'cupboards',
                                 'electrical',
                                 'walls']
        if tileCountertops:
            i = self._inspectionItems.index('countertops')
            self._inspectionItems[i] = 'tileCountertops'
        if sinkWithInsert:
            i = self._inspectionItems.index('sink')
            self._inspectionItems[i] = 'sinkWithInsert'

class LivingRoom(Room):
    def __init__(self, label=None, tileCountertops=False, sinkWithInsert=False, **kwargs):
        super(LivingRoom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'electrical',
                                 'walls',
                                 'cupboards',
                                 'furniture',
                                 ]
        if tileCountertops:
            i = self._inspectionItems.index('countertops')
            self._inspectionItems[i] = 'tileCountertops'
        if sinkWithInsert:
            i = self._inspectionItems.index('sink')
            self._inspectionItems[i] = 'sinkWithInsert'

class Bedroom(Room):
    def __init__(self, label=None, **kwargs):
        super(Bedroom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'closet',
                                 'electrical',
                                 'walls']

class Bathroom(Room):
    def __init__(self, label=None, **kwargs):
        super(Bathroom, self).__init__(label, **kwargs)
        self._inspectionItems = ['cleanliness',
                                 'countertops',
                                 'electrical',
                                 'shower',
                                 'toilet',
                                 'walls']

class Deck(Room): # not really a room, but close enough
    def __init__(self, label=None, **kwargs):
        super(Deck, self).__init__(**kwargs)
        self._inspectionItems = ['cleanliness',
                                 'furniture']

class Basement(Room):
    def __init__(self, **kwargs):
        super(Basement, self).__init__(**kwargs)
        self._inspectionItems = ['general']

class Property(SubjectToInspection):
    def __init__(self, **kwargs):
        self.clauses = {}  # format: {'sectionName': [clause list], ...}
        self.applicationFee = Money(35)
        self.depositNonRefundable = Money(250)
        self.furnished = False
        self.rooms = []
        self.roommateOnly = False
        self.tenantMaintainsYard = True
        self.utilitiesIncluded = []

        super(Property, self).__init__(**kwargs)

        self._required = ['address',
                          'county',
                          'rent',
                          'deposit',
                          'occupantLimit']
    
        # add gas/oil on a per-property basis
        self._inspectionItems = ['smokeDetectors',
                                 'electricMeter',
                                 'waterMeter',
                                 ]


class LeaseContract(Contract):
    def __init__(self, searchPath=None, signatureFilePath=None, **kwargs):
        self.lessors = []
        self.occupants = []
        self.tenants = []
        self.property = None

        self.leaseStartDate = None
        self.leaseEndDate = None
        self.monthToMonth = False
        self.renewal = False
        self.signSections = []

        self.moveInTime = '2:00pm'
        self.moveOutTime = '12:00pm (noon)'
        self.administrativeGracePeriodDays = 7
        self.gracePeriodDays = 5
        self.dailyLatePenalty = Money(25)
        self.latePenaltyLimitPercent = Percent(10)
        self.bouncedCheckPenalty = Money(50)

        self.title = 'Lease/Rental Agreement'
        self.subtitle = "This document is a Lease Agreement (``Agreement'') between Lessor and Tenant for occupation of a residential property."
        
        super(LeaseContract, self).__init__(searchPath, signatureFilePath, **kwargs)

        self._required += ['depositAccountBankName',
                           'depositAccountBankCityState']

    def getSigningPeople(self):
        return self.tenants + self.lessors

    def multipleTenants(self):
        return len(self.tenants) + len(self.occupants) > 1

    def getLessorDefinitions(self, i):
        return self.getPersonDefinitions('Lessor', self.lessors[i], i+1)
    
    def getTenantDefinitions(self, i):
        return self.getPersonDefinitions('Tenant', self.tenants[i], i+1)
    
    def getOccupantDefinitions(self, i):
        # abbreviated version
        person = self.occupants[i]
        label = 'Occupant'
        result = '''
            \definition{%s %d}{%s}
            \definition{%s %d telephone number}{%s}
        ''' % (label, i+1, person.name,
               label, i+1, getattr(person, 'phone', ''))
        return result
    
    def getPersonDefinitions(self, label, person, i):
        result = '''
            \definition{%s %d}{%s}
            \definition{%s %d current or previous address}{%s}
            \definition{%s %d telephone number}{%s}
        ''' % (label, i, person.name,
               label, i, person.address.getFullAddressTex(),
               label, i, getattr(person, 'phone', ''))
        return result
    
    def getNumberOfFooterRows(self):
        numberOfInitialsRows = max(len(self.lessors), len(self.tenants))
        return 2 + numberOfInitialsRows  # 2 for "initials:" label and "page x of y"

    def getInspectionFormContent(self, moveInOrOut):
        # \newcommand{\getInspectionFormContent}[1]{% format: \getInspectionFormContent{moveIn or moveOut}
        result = []
        for room in self.property.rooms:
            result += self.getInspectionContent(str(room), room, moveInOrOut)

        result += self.getInspectionContent('General', self.property, moveInOrOut)
        return '\n'.join(result)

    def getInspectionContent(self, label, thingToInspect, moveInOrOut):
        result = ['\\subsection{%s}' % label]
        for (label, condition) in thingToInspect.getConditionsTuples(moveInOrOut):
            result.append('\\formLine[%s]{%s}' % (condition, label))
        return result

    def generate(self, outputFilename, system, variables={}):
        # override default clauses with property's custom clauses
        for sectionName in self.property.clauses:
            for clause in self.property.clauses[sectionName]:
                self.addClause(sectionName, clause)
        super(LeaseContract, self).generate(outputFilename, system, variables)

