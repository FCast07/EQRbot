def string_parser(pred_dict,s):
    import re

    def parse_for_key(key, reg, st):
        return re.findall(key+reg, st)

    def reg_builder(key):
        r1 = "\(([A-z0-9_]+)\)"
        r2 = "\(([,A-z0-9_]+)\)"

        if len(pred_dict[key]) == 1:
            return r1
        else:
            return r2

    # a dictionary to keep the result
    res = {}
    bindings = {}
    for p in pred_dict.keys(): #value of key to be added to res
        res[p] = parse_for_key(p, reg_builder(p), s)[0].split(',')

        i = 0
        while i < len(res[p]):
            var = pred_dict[p][i]
            if var not in bindings.keys():
                bindings[var] = res[p][i]
            i+=1
    return bindings


# EQR SCHEME
"""
    s: an argument string to parse.
    example input: s = "eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,paracetamol),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,wellbeing)],reachable_goal(controlling_the_virus_negative_effects))"
"""
def eqr(s):
    pred_dict= {"current_state":["R1","R2","R3"], "expert":["E"], "field":["F"], "recommends":["E", "F","T"], "new_state":["S"], "goal":["G"], "promotes":["G","V"]}

    bindings = string_parser(pred_dict,s)

    # the extra _ will be rendered as a space that separates the strings of the explanation
    explanation = """Given the patient's previous health record and the current {} and {} due to {},_
the expertise of the {} in the field of {}_
indicates {} as an effective treatment._
This should lead to the {}_
which will bolster the goal of {}_
and promote the patient's {}.""".format(bindings["R1"],bindings["R2"],bindings["R3"],bindings["E"],bindings["F"],bindings["T"],bindings["S"],bindings["G"],bindings["V"])

    return bindings,explanation



# SF SCHEME for Relevant Field of Expertise
"""
    s: an argument string to parse.
    example input: s = "sf([fields(covid_management,homeopathy),more_relevant(covid_management,homeopathy)],relevant_field(covid_management))"
"""
def sf(s):
    pred_dict= {"fields":["F1","F2"]}

    bindings = string_parser(pred_dict,s)

    explanation = """The treatment has been recommended by an expert in the field of {}._
This scientific field has been identified as more relevant to devise your care than other available fields, such as {}.""".format(bindings["F1"],bindings["F2"])

    return bindings,explanation



#SE SCHEME for Side Effect
"""
    s: an argument string to parse.
    example input: s = "se([treatment(ibuprofen),may_cause_complication(ibuprofen,pregnancy)],not_recommend(ibuprofen))"
"""
def se(s):
    pred_dict= {"treatment":["T"], "may_cause_complication":["T","C"], "not_recommend":["T"]}

    bindings = string_parser(pred_dict,s)

    explanation = """In order to prevent contraindications and side effects, the potential alternative treatment of {} should be avoided during {}._
Therefore, given your condition, {} should not be recommended as a viable alternative, and paracetamol should be assumed instead.""".format(bindings["T"],bindings["C"],bindings["T"])

    return bindings,explanation



#SEXP SCHEME for Expert Reliability
#Notice that the system uses NICE guidelines, as such it considers it as the most reliable source and provide an explanation accordingly
"""
    s: an argument string to parse.
    example input: s = "sexp([experts(nice_guidelines,local_guidelines),more_reliable(nice_guidelines,local_guidelines)],reliable_expert(nice_guidelines))"
"""
def sexp(s):
    pred_dict= {"experts":["E1", "E2"]}

    bindings = string_parser(pred_dict,s)

    explanation = """{} are considered to be a more reliable expert than the {}, the other available expert._
NICE is the acronym for National Institute for health and Care Excellence._
The expertise of the {} provides evidence-based recommendations for health and care in England (more info at https://www.nice.org.uk/guidance).""".format(bindings["E1"],bindings["E2"],bindings["E1"])

    return bindings,explanation




#ALT SCHEME for Alternative Treatments
"""
    s: an argument string to parse.
    example input: s = "alt([eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,paracetamol),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects)),
                        eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,ibuprofen),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects)),
                        alternative(paracetamol,ibuprofen)],
                        attacks(eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,paracetamol),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects)),
                        eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,ibuprofen),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects))))"
"""
def alt(s):
    pred_dict= {"goal":["G"],"alternative":["T1","T2"]}

    bindings = string_parser(pred_dict,s)

    explanation = "Treatment {} and treatment {} bolster the same goal {}, and {} is an alternative to {}; hence, they should not be offered together.".format(bindings["T1"],bindings["T2"],bindings["G"],bindings["T1"],bindings["T2"])

    return bindings,explanation



#TCQ SCHEME for Challenges between AS
"""
    s: an argument string to parse.
    example input: s = "tcq([se([treatment(ibuprofen),may_cause_complication(ibuprofen,pregnancy)],not_recommend(ibuprofen)),
                             eqr([current_state(fever,headache,covid19),expert(nice_guidelines),field(covid_management),recommends(nice_guidelines,covid_management,ibuprofen),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects)),
                             attacks(se([treatment(ibuprofen),may_cause_complication(ibuprofen,pregnancy)],not_recommend(ibuprofen)),
                             eqr([current_state(fever,headache,covid19),expert(nice_guideliness),field(covid_management),recommends(nice_guidelines,covid_management,ibuprofen),new_state(reduction_of_fever_and_headache),goal(controlling_the_virus_negative_effects),promotes(controlling_the_virus_negative_effects,patient_wellbeing)],reachable_goal(controlling_the_virus_negative_effects))))"
"""
def tcq(s):
    pred_dict= {"challenges":["AS1","AS2"]}

    bindings = string_parser(pred_dict,s)

    explanation = "The scheme {} is a critical question of the scheme {}".format(bindings["AS1"],bindings["AS2"])

    return bindings,explanation
