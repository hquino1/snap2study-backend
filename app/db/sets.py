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
