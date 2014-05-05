#!/usr/bin/python
# -*- coding: utf-8 -*-
from latex_python.JinjaBase import escapeTex

# This is the main contract template.
# It includes clauses for most purposes, including conditional checks 
# for most of the basic options I've thought of.

# Generally, anything more specific than what is covered here
# should go into specific property/contract configs
# on an as-needed basis.

# NOTE: this template (and templates in general) assume(s) that the contract object
#       has been fully initialized with property, tenants, dates, etc.

def addContent(contract):

    ############################################################################################
    section = 'Terms of Lease Agreement'
    ############################################################################################
    
    if not contract.property.roommateOnly and contract.multipleTenants():
        contract.addClause(section, 'Primary Tenant', '''
            Tenant 1 (%s) is
            identified as the Primary Tenant, and is responsible for communicating the terms of this
            agreement to all other occupants. The Primary Tenant is responsible for payment,
            communication and coordination between the Lessor and all Occupants. The Lessor may ask for 
            the Primary Tenant's information beyond what is on this Agreement to arrange billing
            accounts with local utility providers, including photo identification.
            ''' % escapeTex(contract.tenants[0]))
    
    if contract.renewal:
        contract.addClause(section, 'Lease Renewal', ''' 
            This lease is a continuation of another agreement between the same Lessor
            and Tenant. 
            Therefore, the Security Deposit will be carried over from the prior
            agreement, rather than being returned and collected again by the Lessor. 
            Any damages assessed from prior agreements between the parties will be either settled 
            as agreed in writing, or will be considered carried forward as damages occurring 
            within the time period and terms of this agreement. 
            For these reasons, the Move-In Inspection Agreement 
            from the Tenant's original move-in will be carried forward to apply to this Agreement.
            The Move-Out Inspection Agreement will not be filled out from the previous Agreement,
            but will also be carried forward.''')
    
    if contract.property.roommateOnly:
        contract.addClause(section, 'Occupation Type', '''
            Tenant is occupying the Property as a roommate. Therefore, references to ``Property'' refer
            to the room being rented, as well as reasonable use of common areas.''')
    else:
        contract.addClause(section, 'Occupation Type', '''
            The Tenant is renting the entire Property. The Tenant is 
            responsible for all areas of the Property, and references to ``Property'' in this Agreement
            refer to all such areas.''')
    
    if contract.renewal:
        depositText = '''
            A combined Security Deposit and move-in fee has already been collected in the amount of
            \\highlight{%s} as part of the Agreement for which
            this is a Renewal.''' % escapeTex(contract.property.deposit)
    else:
        depositText = '''
            To confirm this Agreement, Tenant will make a payment to Lessor
            in the amount of \\highlight{%s} as a combined
            Security Deposit and move-in fee within 
            \\highlight{%d} days of the Lease Agreement
            Date.''' % (escapeTex(contract.property.deposit), contract.administrativeGracePeriodDays)
    contract.addClause(section, 'Security Deposit', depositText + '''
        Of this amount,
        \\highlight{%s} is a
        non-refundable move-in fee, and the
        remaining portion is a security for performance of Tenant's obligations as described in this
        Agreement, including but not limited to payment of rent and cleaning of the Property for which
        Tenant is responsible, and to indemnify Lessor for damage to the Property. If any such damage
        occurs beyond the refundable portion, then the Tenant will be responsible for the difference.
        Values of damages will be based on reasonable market value of any incurred repairs, 
        replacement, or services.
        This deposit will be held in an account at %s in 
        %s.''' % (escapeTex(contract.property.depositNonRefundable),
                  contract.depositAccountBankName,
                  contract.depositAccountBankCityState))
        
    contract.addClause(section, 'Rent', '''
        The rent is \\highlight{%s} per month,
        payable on or before the first of each month commencing on the first month of the lease term. 
        If the Tenant moves in on a date other than the first of the month, then a pro-rated amount for
        the remaining portion of the first month plus one month's rent will be due upon occupation of the
        Property.''' % escapeTex(contract.property.rent))
        
    contract.addClause(section, 'Rent Late Charge/NSF Check', '''
        If any rent is not paid on or before the due date plus a
        \\highlight{%s} day grace period, Tenant
        agrees to pay a late charge of
        \\highlight{%s} for each day the payment
        is delinquent after the last day of the grace period, up to a
        maximum of \\highlight{%s} of one
        month's rent.
        
        Tenant agrees to pay a charge of
        \\highlight{%s} for each
        Non-Sufficient Funds (NSF) check given by Tenant to Lessor. Lessor
        shall have no obligation to redeposit any check returned NSF.
        Lessor may elect to terminate this Agreement for nonpayment of
        rent, including checks returned NSF. Lessor shall notify Tenant of
        late rent and NSF check charges, and charges must be paid within
        \\highlight{%d} days.
        ''' % (escapeTex(contract.gracePeriodDays),
               escapeTex(contract.dailyLatePenalty),
               escapeTex(contract.latePenaltyLimitPercent),
               escapeTex(contract.bouncedCheckPenalty),
               contract.gracePeriodDays))
    
    if contract.property.utilitiesIncluded:
        contract.addClause(section, 'Utilities', '''
            The rent includes reasonable use of:
            \\highlight{%s}.
            Tenant shall pay all other utilities owed when due.
            ''' % escapeTex(', '.join(contract.property.utilitiesIncluded)))
    else:
        contract.addClause(section, 'Utilities', 'No utilities are included in rent.')
    
    if contract.renewal:
        inspectionText = '''
            This Agreement is a Renewal of a prior Agreement, and so shall inherit 
            the move-in inspection agreement from the prior Agreement.'''
    else:
        inspectionText = '''
            Before moving in, the move-in inspection 
            agreement included in this Agreement (section \\ref{moveInInspection})
            will be filled out by Lessor and
            Tenant, and initialed on the bottom of each page. Spaces left blank indicate items
            in good condition and general cleanliness. Each party's initials indicate acknowledgement
            that the state of the property is as documented, and binds each initialed 
            page to this Agreement by the terms
            stated here. 
            Within \\highlight{%d} days of occupation of the Property, 
            if any item differs noticeably from its condition
            as documented in section \\ref{moveInInspection}, Tenant will notify Lessor and
            section \\ref{moveInInspection} will be modified and re-initialed as appropriate.
            ''' % contract.administrativeGracePeriodDays
    contract.addClause(section, 'Inspection Agreements', inspectionText + '''
        Upon vacation or abandonment of Property, Lessor and Tenant will fill out
        the move-out inspection (section \\ref{moveOutInspection}). Spaces left blank indicate items
        in good condition and general cleanliness.
        Any items that differ from their move-in state beyond normal wear and tear shall be
        considered damaged and the value of damages withheld from the Security Deposit
        (clause \\ref{Security Deposit}).
    
        Within \\highlight{%d} days of the Tenant's move-out date,
        Lessor will give Tenant a statement of
        the basis of retaining any of the Deposit, and the remaining balance between the Lessor and Tenant
        will be paid by a method mutually agreed upon between them within 
        \\highlight{%d} days of the move-out date.
        ''' % (contract.administrativeGracePeriodDays,
               # (administrativeGracePeriodDays * 2) gives 1 period for agreement and 1 period for payment
               contract.administrativeGracePeriodDays * 2,
               ))
            
    if not contract.renewal:
        contract.addClause(section, 'Possession', '''
            Tenant may take possession of the property starting at \\highlight{%s}
            on the Occupation Date. Before taking possession, Tenant must have paid the first Rent payment
            as defined in clause \\ref{Rent}, and the payment transaction must be cleared for withdrawal 
            by the Lessor's bank.
            In the event Tenant fails to take possession of the Property within
            \\highlight{%d} days of the Occupation Date, Tenant will forfeit the 
            Security Deposit and this Agreement will become void. If, through no fault of Lessor, Lessor
            cannot deliver possession of the Property to Tenant on the Occupation Date, Lessor shall
            not be liable to Tenant for damages. In this case, rent charges will accrue starting on the date
            possession is taken, unless otherwise agreed upon in writing.
            ''' % (escapeTex(contract.moveInTime),
                   contract.administrativeGracePeriodDays))
    
    if contract.property.roommateOnly:
        occupantsText = '''
            The Tenant is occupying the Property as a roommate, and no
            additional occupants will be allowed without explicit permission from the Lessor.'''
    else:
        occupantsText = '''
            The property is being rented as a private residence only for the Tenant and
            Additional Occupants listed in this Agreement, plus any additional occupant(s) chosen at
            the discretion of the Tenant up to a maximum of 
            \\highlight{%d} total occupants.''' % contract.property.occupantLimit
    contract.addClause(section, 'Authorized Occupants', occupantsText + '''
        The Tenant shall not assign this Agreement,
        sublet all or any portion of the Property, nor give accommodation to any other roomers or
        lodgers, without the prior written consent of the Lessor. Additional occupants may be approved,
        but this may also increase the monthly rent amount. All occupants are bound by the same terms
        as the Tenant.''')
    
    if contract.property.furnished:
        furnitureText = '''
            The property is being rented as a \\textbf{Furnished} residence, and it is the tenant's
            responsibility to protect the included furniture against abnormal wear and tear.'''
    else:
        furnitureText = 'The property is being rented as an \\textbf{Unfurnished} residence.'
    contract.addClause(section, 'Furniture', furnitureText + '''
        It is the tenant's responsibility to protect the walls and floors from damage when moving
        furniture.''')
            
    if contract.property.tenantMaintainsYard:
        maintenanceText = '''
            Tenant will at all times maintain the property, including any yard and lawn, in
            a neat and clean condition. This includes cutting and watering any lawn and watering
            and trimming any shrubs, trees, or landscaping on the Property.'''
    else:
        maintenanceText = ''
    contract.addClause(section, 'Maintenance', maintenanceText + '''
        Upon termination of this agreement, Tenant will leave the Property in as good
        condition as it is now, reasonable wear and tear excepted. Tenant agrees not to make any
        alterations or improvements to the Property without Lessor's prior written approval.''')
    
    contract.addClause(section, 'Entry/Inspection/Maintenance/Sale', '''
        Lessor may enter the Property to inspect it, make
        alterations or repairs, or show it to potential renters or buyers at reasonable times and, except in
        emergencies, will give 24 hours' notice to Tenant before entering.''')
    
    contract.addClause(section, 'Agents', '''
        Lessor may have others (``Agents'') act as their
        representatives for the purposes of executing portions of this Agreement, including 
        interacting with the Tenant, performing inspections and/or maintenance, 
        and enforcing terms of the Agreement. Lessor will notify the Tenant and identify any such 
        Agent before the Agent visits the Property or
        otherwise makes contact with the Tenant. Without this notice, other parties should 
        not be considered to have any special privileges.''')
    
    if contract.monthToMonth:
        terminationText = '''
            This is a month-to-month lease, and the Termination Date (section 
            \\ref{terminationSignatures}) is used to indicate
            the move-out date. Tenant must give 20 days' notice to Lessor when moving out.'''
    else:
        terminationText = '''
            This is a fixed-length lease, and the Termination Date is defined by the
            Lease End Date (definition \\ref{Lease End Date}).'''
    contract.addClause(section, 'Termination', terminationText + '''    
        If not signing another subsequent lease for the same property,
        Tenant is instructed to move out by \\highlight{%s} on the 
        Termination Date at the latest. Upon termination of this Agreement, 
        any remaining financial obligations of
        Lessor or Tenant as defined by the Agreement remain intact and payable.
        ''' % escapeTex(contract.moveOutTime))
        
    contract.addClause(section, "Attorney's Fees", '''
        If at any time it becomes necessary for Lessor or
        Tenant to employ an attorney to enforce any terms of this Agreement, the prevailing party is
        entitled to reasonable attorneys' fees as provided for by law. In the event of a trial, the amount
        shall be as fixed by the Court.''')
    
    contract.addClause(section, 'Waiver of Subrogation', '''
        Lessor and Tenant hereby release and waive, for the duration of
        this Agreement and any extension or renewal thereof, their respective rights of recovery against
        each other for any loss resulting from perils of fire and/or extended coverage as defined in
        fire insurance policies issued to either Lessor or Tenant in effect at the time of loss,
        provided that such waiver and resale shall apply only in the event such agreement does not
        prejudice the insurance afforded by such policies.''')
    
    contract.addClause(section, 'Personal Property', '''
        Tenant agrees that all personal property kept in or on the Property is at
        the risk of the Tenant. Tenant is specifically advised of the availability of Renters' Insurance,
        and is encouraged to obtain insurance for such personal property.''')
    
    if contract.renewal:
        smokeDetectorText = '''
            This Agreement is a Renewal, and the Tenant agrees that prior to this Agreement,
            the smoke detector(s) have been in operation and are now the responsibility of the Tenant.'''
    else:
        smokeDetectorText = '''
            The detector(s) will be tested during the
            Move-In Inspection (section \\ref{moveInInspection}), and any non-operational detectors will
            be repaired or replaced.'''
    contract.addClause(section, 'Smoke Detector', '''
        Tenant acknowledges and Lessor certifies that the Property is equipped with
        a smoke detector(s) as required by RCW 43.44.110.
        
        %s  
        It is Tenant's responsibility to maintain the smoke detector(s) as specified by
        the manufacturer, including replacement of batteries, if required. Failure to properly maintain the
        smoke detector(s) can result in punishment including a fine pursuant to
        RCW 43.44.110.''' % smokeDetectorText)
        
    ############################################################################################
    section = 'Rules'
    ############################################################################################
    
    contract.addClause(section, 'Garbage', '''
        Tenant shall furnish garbage can(s) if not supplied by garbage
        collection company, and place it/them where necessary for collection, or shall deliver garbage
        to collection bins if Property is part of a multi-unit building and garbage is collected
        centrally. Any excess garbage fees incurred because of Tenant's garbage will be payable by Tenant,
        even if these charges are billed after the Move-Out Date.''')
    
    contract.addClause(section, 'Illegal Use', '''
        Tenant shall not use the Property for any illegal purposes.''')
    
    contract.addClause(section, 'Repairs', '''
        Tenant shall promptly repair, at Tenant's expense, any damaged glass or screens in doors or
        windows, as well as any broken light bulbs or other items which by their design require periodic
        replacement.''')
    
    if contract.property.tenantMaintainsYard:
        contract.addClause(section, 'Snow', '''
            In the event of snow, Tenant shall remove snow from any abutting sidewalks.''')
            
#     contract.addClause(section, 'Freezing', '''
#         Tenant shall protect the plumbing from freezing. As a minimum, Tenant shall
#         leave the heat on low during cold weather, and operate various plumbing fixtures occasionally to
#         keep water flowing.''')
#     
    contract.addClause(section, 'Drains', '''
        Tenant shall use a hair trap in bathtub during showers to prevent clogging of
        drain. Tenant shall relieve stoppage of drains and sewers at Tenant's expense unless resulting
        from a condition existing at the Occupation Date.''')
    
    contract.addClause(section, 'Nails/Painting', '''
        Tenant shall not drive any nails or screws into walls, and shall not
        paint anything, without the prior written consent of the Lessor.''')
    
    contract.addClause(section, 'Noise/Nuisance', '''
        TV, music, and other sound volumes shall be kept low enough so that no
        noise whatsoever shall escape from the Property. Tenant shall not create or permit any other
        nuisance on the Property.''')
    
    contract.addClause(section, 'Guests', '''
        Tenant is responsible for the conduct of all guests on the Property and shall
        ensure that guests comply with these Rules.''')
    
    contract.addClause(section, 'Pets', '''
        No dogs, cats or other animals will be permitted on the Property without the prior
        written consent of the Lessor. If lessor has given written permission for pets on the
        property, no pet noise whatsoever shall be allowed to escape from the Property. In the case
        of apartments/condominium units, pets shall not be allowed in the hallways, common spaces
        or surrounding property except on a leash and accompanied by the Tenant. It is the Tenant's
        responsibility to clean up and dispose of any pet excrement anywhere on the Property and
        adjacent sidewalks, streets, alleys, and neighbors' properties.''')
    
    contract.addClause(section, 'Vehicles', '''
        Recreation vehicles, trailers, boats and inoperable or unlicensed automobiles
        may not be parked or stored on the Property, on or in any parking area provided for the
        Property, or on any street or alley serving the Property. Repairs to any vehicles in these
        locations must be completed within 24 hours of commencement.''')
    
    contract.addClause(section, 'Fireplace Insert/Wood Stove', '''
        Wood stoves are prohibited, unless provided by Lessor. No
        fireplace insert may be installed without Lessor's prior written permission. If permission is
        given, then the installation must be inspected by the applicable city or county building
        department, at Tenant's expense, before it is used.''')
    
    contract.addClause(section, 'Water Beds, Pianos and Heavy Objects', '''
        No water beds, aquariums, pianos, organs,
        libraries, or other unusually heavy objects are permitted in the Property without Lessor's
        written permission. As a condition to permitting a water bed, Lessor may require Tenant to
        provide and pay for water bed insurance.''')
