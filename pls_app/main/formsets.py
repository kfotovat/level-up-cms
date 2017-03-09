from django.forms.models import BaseInlineFormSet, inlineformset_factory, BaseModelFormSet, modelformset_factory
from django.forms.formsets import BaseFormSet, formset_factory
from .models import Teacher, Course
from .forms import TeacherForm
# , TeacherProgressForm

# formset_factory should inherit from BaseFormSet (django.forms.formsets)
# modelformset_factory should inherit from BaseModelFormSet
# inlineformset_factory should inherit from BaseInlineFormSet

class ModifiedFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(ModifiedFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
        	# write out modifications here
         	form.empty_permitted = False


# ProgressFormset = formset_factory(TeacherProgressForm, extra=5)
    CourseFormset = inlineformset_factory(
    	Teacher,
    	Course,
    	formset=BaseInlineFormSet,
    	form=TeacherForm,
    	fields=['block_order','course_name', 'start_time', 'end_time']
    	)
