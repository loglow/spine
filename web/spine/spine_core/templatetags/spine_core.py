# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def object_count_string(value, arg):
    if value == '0':
        return 'No '+arg+'s'
    elif value == '1':
        return value+' '+arg
    else:
        return value+' '+arg+'s'

@register.filter(is_safe=True)
@stringfilter
def under_to_space(value):
    return value.replace('_', ' ')