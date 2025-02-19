from playwright.sync_api import sync_playwright,Page
from fractions import Fraction
import time,re,math
with open('credentials') as f:
    _=f.read().split('\n')
    USERNAME=_[0]
    PASSWORD=_[1]
    del _





def replace_operators(equation:str,)->str:
    return equation.replace('×','*').replace('·','*').replace('÷','/').replace('−','-')
def remove_answer_box(equation:str)->str:
    return equation.replace('_','').strip().replace('  ','').replace('  ','')

"Levels 1-3 are very simple and can use the function"
def level_1(equation:str)->int|float:
    return eval(remove_answer_box(replace_operators(equation)).strip().rstrip('='))
def level_2(equation:str)->int|float:
    return level_1(equation)
"Level 3 is a more complex and requires parsing"
def level_3(equation:str)->int|float:
    equation=replace_operators(equation.lower())
    if 'half' in equation:
        match=re.search(r'half of (\d+)',equation)
        if match:
            return int(match.group(1))//2
    equation=equation.replace(' ','')

    # if level 1 works, then great! otherwise, use simple algebra
    try:return level_1(equation)
    except:0
    simple_algebra=re.search(r'(\d+)(\+|-|\*|/)_=(\d+)',equation.replace(' ',''))
    if simple_algebra:
        print(simple_algebra.groups())
        a=float(simple_algebra.group(1))
        b=float(simple_algebra.group(3))
        operator=simple_algebra.group(2)
        if operator=='+':
            return b-a
        if operator=='-':
            return b+a
        if operator=='*':
            return b//a
        if operator=='/':
            return b*a
    return 0

def level_4(equation:str)->int|float:
    return level_3(equation)

"Level 5 is much more difficult including conversions between metric system units and time, but still contains equations from previous levels"
def level_5(equation:str)->int|float: # btw, thank you github copilot for making this function 10x easier to make!
    equation=remove_answer_box(replace_operators(equation.lower()))
    # if level 4 works, good
    try:return level_4(equation)
    except:0

    # time for regex... a lot of it

    # How many minutes in [__] hours

    if 'how many minutes in' in equation or 'how many minutes is' in equation:
        match=re.search(r'how many minutes i(n|s) (\d+) hours',equation)
        if match:
            return int(match.group(2))*60

    # How many hours in [__] minutes

    if 'how many hours in' in equation or 'how many hours is' in equation:
        match=re.search(r'how many hours i(n|s) (\d+) minutes',equation)
        if match:
            return int(match.group(2))//60

    # How many seconds in [__] minutes

    if 'how many seconds in' in equation or 'how many seconds is' in equation:
        match=re.search(r'how many seconds i(n|s) (\d+) minutes',equation)
        if match:
            return int(match.group(2))*60

    # How many minutes in [__] seconds

    if 'how many minutes in' in equation or 'how many minutes is' in equation:
        match=re.search(r'how many minutes i(n|s) (\d+) seconds',equation)
        if match:
            return int(match.group(2))//60

    # Fuckk.. i got to do the metric conversion :( (btw, thank you copilot for doing this for me!)
    try:
        metric=re.search(r'(\d+)( |)(cm|mm|km|m|g|kg|mg|t|l|ml)( |)=( |)(cm|mm|km|m|g|kg|mg|t|l|ml)',equation)
        if metric:
            digit=float(metric.group(1))
            current_unit=metric.group(3)
            unit_to_convert_to=metric.group(6)
            if current_unit=='cm':
                if unit_to_convert_to=='mm':
                    return digit*10
                if unit_to_convert_to=='m':
                    return digit/100
                if unit_to_convert_to=='km':
                    return digit/100000
            if current_unit=='mm':
                if unit_to_convert_to=='cm':
                    return digit/10
                if unit_to_convert_to=='m':
                    return digit/1000
                if unit_to_convert_to=='km':
                    return digit/1000000
            if current_unit=='m':
                if unit_to_convert_to=='cm':
                    return digit*100
                if unit_to_convert_to=='mm':
                    return digit*1000
                if unit_to_convert_to=='km':
                    return digit/1000
            if current_unit=='km':
                if unit_to_convert_to=='cm':
                    return digit*100000
                if unit_to_convert_to=='mm':
                    return digit*1000000
                if unit_to_convert_to=='m':
                    return digit*1000
            if current_unit=='g':
                if unit_to_convert_to=='mg':
                    return digit*1000
                if unit_to_convert_to=='kg':
                    return digit/1000
                if unit_to_convert_to=='t':
                    return digit/1000000
            if current_unit=='mg':
                if unit_to_convert_to=='g':
                    return digit/1000
                if unit_to_convert_to=='kg':
                    return digit/1000000
                if unit_to_convert_to=='t':
                    return digit/1000000000
            if current_unit=='kg':
                if unit_to_convert_to=='mg':
                    return digit*1000000
                if unit_to_convert_to=='g':
                    return digit*1000
                if unit_to_convert_to=='t':
                    return digit/1000
            if current_unit=='t':
                if unit_to_convert_to=='mg':
                    return digit*1000000000
                if unit_to_convert_to=='g':
                    return digit*1000000
                if unit_to_convert_to=='kg':
                    return digit*1000
            if current_unit=='l':
                if unit_to_convert_to=='ml':
                    return digit*1000
            if current_unit=='ml':
                if unit_to_convert_to=='l':
                    return digit/1000
    except:0

    # mathletics is a pain, it does metric on both sides of the equation, so we have to do it twice

    try:
        metric=re.search(r'(cm|mm|km|m|g|kg|mg|t|l|ml)( |)=( |)(\d+)( |)(cm|mm|km|m|g|kg|mg|t|l|ml)',equation)
        if metric:
            unit_to_convert_to=metric.group(1)
            current_unit=metric.group(6)
            digit=float(metric.group(4))
            if current_unit=='cm':
                if unit_to_convert_to=='mm':
                    return digit*10
                if unit_to_convert_to=='m':
                    return digit/100
                if unit_to_convert_to=='km':
                    return digit/100000
            if current_unit=='mm':
                if unit_to_convert_to=='cm':
                    return digit/10
                if unit_to_convert_to=='m':
                    return digit/1000
                if unit_to_convert_to=='km':
                    return digit/1000000
            if current_unit=='m':
                if unit_to_convert_to=='cm':
                    return digit*100
                if unit_to_convert_to=='mm':
                    return digit*1000
                if unit_to_convert_to=='km':
                    return digit/1000
            if current_unit=='km':
                if unit_to_convert_to=='cm':
                    return digit*100000
                if unit_to_convert_to=='mm':
                    return digit*1000000
                if unit_to_convert_to=='m':
                    return digit*1000
            if current_unit=='g':
                if unit_to_convert_to=='mg':
                    return digit*1000
                if unit_to_convert_to=='kg':
                    return digit/1000
                if unit_to_convert_to=='t':
                    return digit/1000000
            if current_unit=='mg':
                if unit_to_convert_to=='g':
                    return digit/1000
                if unit_to_convert_to=='kg':
                    return digit/1000000
                if unit_to_convert_to=='t':
                    return digit/1000000000
            if current_unit=='kg':
                if unit_to_convert_to=='mg':
                    return digit*1000000
                if unit_to_convert_to=='g':
                    return digit*1000
                if unit_to_convert_to=='t':
                    return digit/1000
            if current_unit=='t':
                if unit_to_convert_to=='mg':
                    return digit*1000000000
                if unit_to_convert_to=='g':
                    return digit*1000000
                if unit_to_convert_to=='kg':
                    return digit*1000
            if current_unit=='l':
                if unit_to_convert_to=='ml':
                    return digit*1000
            if current_unit=='ml':
                if unit_to_convert_to=='l':
                    return digit/1000
    except:0

    # yet again, mathletics decides to have a "no digit" conversion. i.e. `cm = m` and you figure it out
    try:
        metric=re.search(r'(cm|mm|km|m|g|kg|mg|t|l|ml)( |)=( |)(cm|mm|km|m|g|kg|mg|t|l|ml)',equation)
        if metric:
            unit_to_convert_to=metric.group(1)
            current_unit=metric.group(4)
            if current_unit==unit_to_convert_to:
                return 1
            if current_unit=='cm':
                if unit_to_convert_to=='mm':
                    return 10
                if unit_to_convert_to=='m':
                    return 0.01
                if unit_to_convert_to=='km':
                    return 0.00001
            if current_unit=='mm':
                if unit_to_convert_to=='cm':
                    return 0.1
                if unit_to_convert_to=='m':
                    return 0.001
                if unit_to_convert_to=='km':
                    return 0.000001
            if current_unit=='m':
                if unit_to_convert_to=='cm':
                    return 100
                if unit_to_convert_to=='mm':
                    return 1000
                if unit_to_convert_to=='km':
                    return 0.001
            if current_unit=='km':
                if unit_to_convert_to=='cm':
                    return 100000
                if unit_to_convert_to=='mm':
                    return 1000000
                if unit_to_convert_to=='m':
                    return 1000
            if current_unit=='g':
                if unit_to_convert_to=='mg':
                    return 1000
                if unit_to_convert_to=='kg':
                    return 0.001
                if unit_to_convert_to=='t':
                    return 0.000001
            if current_unit=='mg':
                if unit_to_convert_to=='g':
                    return 0.001
                if unit_to_convert_to=='kg':
                    return 0.000001
                if unit_to_convert_to=='t':
                    return 0.000000001
            if current_unit=='kg':
                if unit_to_convert_to=='mg':
                    return 1000000
                if unit_to_convert_to=='g':
                    return 1000
                if unit_to_convert_to=='t':
                    return 0.001
            if current_unit=='t':
                if unit_to_convert_to=='mg':
                    return 1000000000
                if unit_to_convert_to=='g':
                    return 1000000
                if unit_to_convert_to=='kg':
                    return 1000
            if current_unit=='l':
                if unit_to_convert_to=='ml':
                    return 1000
            if current_unit=='ml':
                if unit_to_convert_to=='l':
                    return 0.001
    except:0

    return '-400000'

"Level 6 is basically word problems, but with the help of `levels.json`, i might be able to figure it out"
def level_6(equation:str)->int|float:
    # Sequences: whole numbers
        # this is harder bc it includes multiplication
        # for some reason, this only works if it is first
    nospace=equation.replace(' ','')
    blank_pos_3=re.match(r'(\d+),(\d+),_,(\d+)(?!\.)',nospace) # could be addition or multiplication
    if blank_pos_3:
        a=int(blank_pos_3.group(1))
        b=int(blank_pos_3.group(2))
        c=int(blank_pos_3.group(3))
        _change=b-a
        if a+_change*3==c: # then its 'linear'
            return a+_change*2
        return a*(b/a)**2

    blank_pos_4=re.match(r'(\d+),(\d+),(\d+),_',nospace) # only multiplication
    if blank_pos_4:
        a=int(blank_pos_4.group(1))
        b=int(blank_pos_4.group(2))
        return a*(b/a)**3
    blank_pos_2=re.match(r'(\d+),_,(\d+),(\d+)(?!\.)',nospace) # this *would* interfere with blank_pos_3, but since it is after it, it doesnt. (looks like mult, but actually linear)
    if blank_pos_2:
        a=int(blank_pos_2.group(1))
        b=int(blank_pos_2.group(2))
        c=int(blank_pos_2.group(3))
        if a+b==c: # then its 'linear'
            return a*2
        return a*math.sqrt(b/a)

    # Sequences: decimals
        # blank positions in order with `levels.json`
    blank_pos_4=re.match(r'(\d+\.\d+|\d+),(\d+\.\d+|\d+),(\d+\.\d+|\d+),_',nospace)
    blank_pos_2=re.match(r'(\d+\.\d+|\d+),_,(\d+\.\d+|\d+),(\d+\.\d+|\d+)',nospace)
    blank_pos_3=re.match(r'(\d+\.\d+|\d+),(\d+\.\d+|\d+),_,(\d+\.\d+|\d+)',nospace)
    if blank_pos_4:
        a=float(blank_pos_4.group(1))
        b=float(blank_pos_4.group(2))
        change=b-a
        return a+change*3
    if blank_pos_2:
        a=float(blank_pos_2.group(1))
        b=float(blank_pos_2.group(2))
        change=(b-a)/2
        return a+change
    if blank_pos_3:
        a=float(blank_pos_3.group(1))
        b=float(blank_pos_3.group(2))
        change=b-a
        return a+change*2

    try:
        l5=level_5(equation)
        if l5 != '-400000':
            return l5
    except:0

    equation=replace_operators(equation.lower())
    # Simple Percentages
    if '% of' in equation:
        parsed=re.search(r'(\d+)% of (\d+) = _',equation)
        a=parsed.group(1)
        b=parsed.group(2)
        return int(a)/100*int(b)

    # 24 hour time
    if ':00 pm in 24 hour time is' in equation:
        parsed=re.search(r'(\d+):00 pm in',equation)
        a=parsed.group(1)
        return int(a)+12
    if ':00 is the same time as' in equation:
        parsed=re.search(r'(\d+):00 is',equation)
        a=parsed.group(1)
        return int(a)-12

    # Timetable calculations
    min_apart=re.search(r'(cars|boats|trains|trams|aeroplanes|ferries|airplanes) (arriving|leaving) at (\d+):(\d+) (a|p)m and (\d+):(\d+)',equation) # matches for `questions` 1-2
    if min_apart:
        hour_1=int(min_apart.group(3))
        min_1=int(min_apart.group(4))
        time_1=hour_1*60 + min_1
        hour_2=int(min_apart.group(6))
        min_2=int(min_apart.group(7))
        time_2=hour_2*60 + min_2
        return abs(time_1-time_2)

    hour_apart=re.search(r'(buses|taxis|trains|ferries|aeroplanes|airplanes|trams) (arriving|departing) at (\d+):(\d+)( am|) and (\d+):(\d+)( pm|)',equation)
    if hour_apart:
        hour_1=int(hour_apart.group(3))
        min_1=int(hour_apart.group(4))
        hours_1=hour_1+min_1/60
        is_am_to_pm=hour_apart.group(5).strip()=='am' # add 12 if so
        hour_2=int(hour_apart.group(6))+(12*is_am_to_pm)
        min_2=int(hour_apart.group(7))
        hours_2=hour_2+min_1/60
        return round((
            hours_2-hours_1
        )*100)/100
    
    # Fractions and decimals
    as_decimal=re.search(r'(\d+)/(\d+) as a decimal is',equation)
    if as_decimal:
        a=int(as_decimal.group(1))
        b=int(as_decimal.group(2))
        return round((a/b)*1000)/1000
    fraction_simplified=re.search(r'the (denominator|numerator) for 0\.(\d+)',equation)
    if fraction_simplified:
        fraction=Fraction('0.'+fraction_simplified.group(2))
        return fraction.numerator if fraction_simplified.group(1)=='numerator' else fraction.denominator
    
    # Percentages and decimals
    percent_vs_decimal=re.search(r'(\d+)% as a decimal',equation)
    if percent_vs_decimal:
        return float(int(percent_vs_decimal.group(1))/100)
    percent_vs_decimal=re.search(r'(\d+\.\d+|\d+) as a percentage',equation)
    if percent_vs_decimal:
        return float(percent_vs_decimal.group(1))*100
    
    
    return '-400000'

"Level 7 is *mostly* geometry and 3d geometry"
def level_7(equation:str)->int|float:
    try:
        l6=level_6(equation)
        if l6!='-400000':return l6
    except:0
    equation=replace_operators(equation.lower())
    nospace=equation.replace(' ','')

    # Sum, difference, product and quotient
    sdpq=re.match(r'find the (sum|difference|product|quotient) of (\d+) and (\d+)',equation) # acronym
    if sdpq:
        operation=sdpq.group(1)
        a=int(sdpq.group(2))
        b=int(sdpq.group(3))
        if operation=='sum':
            return a+b
        if operation=='difference':
            return a-b
        if operation=='product':
            return a*b
        return a/b # if nothing left, then its quotient
    
    # Cubes
    if '³' in equation:
        cube_match=re.match(r'(\(|)(\d+|-\d+)(\)|)³',nospace)
        if cube_match:
            n=int(cube_match.group(2))
            return n**3
    
    # Volume and capacity conversions
    volume_match=re.match(r'(\d+)(cm³|ml|l)=_(cm³|ml|l)',nospace)
    if volume_match:
        a=int(volume_match.group(1))
        current_unit=volume_match.group(2)
        convert_to_unit=volume_match.group(3)
        if current_unit=='l': # i know it has to be cm³
            return a*1000
        if convert_to_unit == 'l': # i also know it has to be cm³
            return a/1000
        return a # it is the same because cm³ = ml

    # The Cartesian plane
    if 'is in quadrant' in equation:
        cartesian_match=re.match(r'\((\d+|-\d+),(\d+|-\d+)\) is in quadrant',equation)
        x=int(cartesian_match.group(1))
        y=int(cartesian_match.group(2))
        if x>0 and y>0:
            return 1
        if x<0 and y>0:
            return 2
        if x<0 and y<0:
            return 3
        if x>0 and y<0:
            return 4
    
    # Equivalent fractions
    e_fractions=re.match(r'([1-4])/(\d+)=(_|\d+)/(_|\d+)',nospace)
    if e_fractions:
        numerator_1=int(e_fractions.group(1))
        denom_1=int(e_fractions.group(2))
        numerator_2=e_fractions.group(3)
        denom_2=e_fractions.group(4)
        if numerator_2=='_':
            return numerator_1*(int(denom_2)/denom_1) # its nice that
        return denom_1*(int(numerator_2)/numerator_1) # these line up

    # Ratios
    ratio_match=re.match(r'(\d+):(\d+)=(\d+):_',nospace)
    if ratio_match:
        a=int(ratio_match.group(1))
        b=int(ratio_match.group(2))
        c=int(ratio_match.group(3))
        d=b*c/a
        return d
    
    ratio_match=re.match(r'(\d+):(\d+)=_:(\d+)',nospace)
    if ratio_match:
        # print(ratio_match)
        a=int(ratio_match.group(1))
        b=int(ratio_match.group(2))
        d=int(ratio_match.group(3))
        # print(a,b,d)
        c=a*d/b
        return c
    
    ratio_match=re.match(r'_:(\d+)=(\d+):(\d+)',nospace)
    if ratio_match:
        b=int(ratio_match.group(1))
        c=int(ratio_match.group(2))
        d=int(ratio_match.group(3))
        a=c*(b/d)
        return a
    
    ratio_match=re.match(r'(\d+):(\d+):(\d+)=(\d+):_:(\d+)',nospace)
    if ratio_match:
        a=int(ratio_match.group(1))
        b=int(ratio_match.group(2))
        c=int(ratio_match.group(3))
        d=int(ratio_match.group(4))
        f=int(ratio_match.group(5))
        e=b*(f/c)
        return e

    # Volume of rect prisms
    if 'a rectangular prism is' in equation:
        rect_prism=re.match(r'a rectangular prism is (\d+)(mm|cm|m) by (\d+)(mm|cm|m) by (\d+)(mm|cm|m)',equation)
        return int(rect_prism.group(1))*int(rect_prism.group(3))*int(rect_prism.group(5))
    if 'a right-prism' in equation:
        right_prism=re.match(r'a right-prism (\d+)(mm|cm|m) high has a cross-section area of (\d+)',equation)
        a=int(right_prism.group(1))
        b=int(right_prism.group(3))
        return a*b
    rect_area=re.match(r'a rectangle is (\d+)(mm|cm|m) by (\d+)',equation)
    if rect_area:
        w=int(rect_area.group(1))
        h=int(rect_area.group(3))
        return w*h
    triangle_area=re.match(r'a triangle has a base of (\d+)(mm|cm|m) and height (\d+)',equation)
    if triangle_area:
        b=int(triangle_area.group(1))
        h=int(triangle_area.group(3))
        return b*h/2
    square_area=re.match(r'a square has side lengths of (\d+)',equation)
    if square_area:
        return int(square_area.group(1))**2
    
    parallelogram_area=re.match(r'a parallelogram has sides (\d+)(mm|cm|m) that are (\d+)',equation)
    if parallelogram_area:
        a=int(parallelogram_area.group(1))
        b=int(parallelogram_area.group(3))
        return a*b

    return 0

"Holy cow, this gets much harder (also, all of the notes above are written before the function is made, and harder based on how monotonous the code is)"
def level_8(equation:str)->int|float:
    # Recurring decimals
    equation=replace_operators(equation.lower())
    nospace=equation.replace(' ','')

    recurring_decimals=re.match(r'0\.(\d)(\d)(\d)...=_/(\d)',nospace)
    if recurring_decimals:
        n=int(recurring_decimals.group(1))
        d=int(recurring_decimals.group(4)) # either 3 or 9
        if d==3:
            return n/3
        return n
    
    # Substitution (frick i hate this one (not bc its hard but because its annoying, yes i could have included (+|-) to get the sign, but no, i didnt feel like it))
     # 2 vars (xy)
    subst=re.match(r'find x \+ y if x = (\d+) and y (\d+)',equation)
    if subst:return int(subst.group(1))+int(subst.group(2))
    subst=re.match(r'find x - y if x = (\d+) and y (\d+)',equation)
    if subst:return int(subst.group(1))-int(subst.group(2))

     # 3 vars (xyz)
    subst=re.match(r'find x \+ y \+ z if x = (\d+), y (\d+) and z = (\d+)',equation)
    if subst:return int(subst.group(1))+int(subst.group(2))+int(subst.group(3))
    subst=re.match(r'find x - y \+ z if x = (\d+), y (\d+) and z = (\d+)',equation)
    if subst:return int(subst.group(1))-int(subst.group(2))+int(subst.group(3))
    subst=re.match(r'find x - y - z if x = (\d+), y (\d+) and z = (\d+)',equation)
    if subst:return int(subst.group(1))-int(subst.group(2))-int(subst.group(3))

     # 3 vars (abc)
    subst=re.match(r'find a - \(b \+ c\) if a = (\d+), b (\d+) and c = (\d+)',equation)
    if subst:return int(subst.group(1))-int(subst.group(2))-int(subst.group(3))
    subst=re.match(r'find a - \(b - c\) if a = (\d+), b (\d+) and c = (\d+)',equation)
    if subst:return int(subst.group(1))-int(subst.group(2))+int(subst.group(3))
    subst=re.match(r'find \(b \+ c\) - a if a = (\d+), b (\d+) and c = (\d+)',equation)
    if subst:return int(subst.group(2))-int(subst.group(3))-int(subst.group(1))
    
    # Stats
    stats=re.match(r'the mean score of (\d+) and (\d+)',equation)
    if stats:return (int(stats.group(1))+int(stats.group(2)))/2
    stats=re.match(r'the mean score of (\d+), (\d+), (\d+) and (\d+)',equation)
    if stats:return (int(stats.group(1))+int(stats.group(2))+int(stats.group(3))+int(stats.group(4)))/4
    stats=re.match(r'the mode of the scores (\d+),(\d+),(\d+),(\d+) and (\d+)',equation)
    if stats:return int(stats.group(0)) # the way mathletics is, the first and middle terms are the mode
    stats=re.match(r'the median score of (\d+),(\d+),(\d+),(\d+) and (\d+)',equation)
    if stats:return int(stats.group(4)) # from the mathletics answers
    stats=re.match(r'the range of scores (\d+),(\d+),(\d+),(\d+) and (\d+)',equation)
    if stats:return int(stats.group(4))-int(stats.group(2)) # mathelics just works this way

    # Simplifying algebra
    "... I'll.... figure this out later" " its not too complex but i just dont feel like it rn"
    



def run(parsing_method,repeat=1,between=0.025,*,log=False,speed=False,wait_for_equation=True):
    log=False if speed else log
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context('Browser/browser_data',headless=False)
        page:Page = browser.new_page()
        page.goto("https://sign-in.mathletics.com/")
        page.wait_for_selector('button[type="submit"]')
        # Sign in
        page.fill('#userName', USERNAME)
        page.fill('#password', PASSWORD)
        page.click('button[type="submit"]')

        print('\nGo to live mathletics and then start.')

        equation_selector='.questions-text-alignment.whiteTextWithShadow'
        answer_selector='[ng-model="innerAnswerInput"]'

        def _get_equation():
            page.wait_for_selector(equation_selector,timeout=5000)
            equation_element=page.query_selector(equation_selector)
            equation=equation_element.inner_text()
            equation=re.sub(r'<input.*>','_',equation_element.inner_html()).replace('  ',' ').replace('  ',' ')
            return equation
        for _ in range(repeat):
            input('Press Enter to start...')
            time.sleep(1)
            start=time.perf_counter()
            questions_answered=0
            last_equation=None
            last_answer=None
            while True:
                try:
                    equation=_get_equation()
                    if equation==last_equation and wait_for_equation:
                        if log:print('Slowing down... Mathletics cannot keep up.')
                        time.sleep(0.2)

                    if log:print('Found equation:',equation)

                    try:
                        answer=parsing_method(equation.strip())
                        answer=round(answer*1000)/1000
                        if answer==int(answer):
                            answer=int(answer)
                        if log:print('Got answer:',answer)
                    except Exception as e:
                        if log:print(e) # so if something happens (weird or not), it continues
                    
                    page.fill(answer_selector,str(answer))
                    page.press(answer_selector,'Enter')
                    questions_answered+=1
                    if not speed:time.sleep(between)
                    last_equation=equation
                except Exception as e:
                    if log:print(e)
                    break
            print('Time taken:',time.perf_counter()-start-30) # subract 30 for timeouts
            print('Questions answered:',questions_answered)
            print('Questions Per Second:',questions_answered/(time.perf_counter()-start))
        # Wait for user to close the browser
        input('Press Enter to close the browser...')

if __name__=='__main__':
    RUN=1
    print(level_3('18 + _ = 20 '))
    if RUN:
        QPS=2.23
        run(level_3,between=1/QPS,log=True)