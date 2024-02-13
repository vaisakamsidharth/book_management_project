from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    total_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def get_books_count(self):
        """
        Method to get the number of books written by the author.
        """
        return self.books.count()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    total_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to update the total_rating of the associated Author or Book.
        """
        super().save(*args, **kwargs)
        if self.author:
            # Calculate the number of reviews for the author
            reviews_count = Review.objects.filter(author=self.author).count()
            # Update the total_rating of the author
            self.author.total_rating = (self.author.total_rating + self.rating) / (reviews_count + 1)
            self.author.save()
        elif self.book:
            # Calculate the number of reviews for the book
            reviews_count = Review.objects.filter(book=self.book).count()
            # Update the total_rating of the book
            self.book.total_rating = (self.book.total_rating + self.rating) / (reviews_count + 1)
            self.book.save()

    def __str__(self):
        return f"Rating: {self.rating} - Comment: {self.comment}"