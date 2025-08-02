from supabase import Client


def get_sets(supabase: Client, user_id):

    flashcards = (
        supabase.from_("Sets")
        .select("title", "created_at", "set_id")
        .eq("type", "Flashcards")
        .execute()
    )

    practiceExams = (
        supabase.from_("Sets")
        .select("title", "created_at", "set_id")
        .eq("type", "PracticeExam")
        .execute()
    )
    
    return flashcards.data, practiceExams.data

def get_set_content_by_id(supabase: Client, setId, studyMethod):
    
    title = (
        supabase.from_("Sets")
        .select('title')
        .eq("set_id", setId)
        .execute()
    )

    match studyMethod:

        case "Flashcards":
            flashcards = (
                supabase.from_(studyMethod)
                .select('question, answer')
                .eq("set_id", setId)
                .execute()
            )

            return flashcards.data, title.data[0]["title"]
        
        case "PracticeExam":
            practiceExam = (
                supabase.from_("ExamQuestions")
                .select('question, a1, a2, a3, a4, correct')
                .eq("set_id", setId)
                .execute()
            )

            return practiceExam.data, title.data[0]["title"]