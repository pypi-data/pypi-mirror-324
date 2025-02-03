"""Data Generator Layer"""
import functools
import logging

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from sage_tools.repository.generator import BaseDataGenerator

try:
    from tqdm import tqdm
except ImportError as exc:
    raise ImportError("Install `tqdm` package. Run `pip install tqdm`.") from exc

from sage_blog.models import Post, PostCategory, PostFaq, PostTag

logger = logging.getLogger(__name__)
User = get_user_model()


class DataGeneratorLayer(BaseDataGenerator):
    """Data Generator Layer

    DGL is a layer to use anywhere in source code to generate data for blog app.
    Use Cases:
    - Test Cases
    - manage.py blog_data_generator
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_tags(self, total, batch_size=300, disable_progress_bar=False):
        """Create tag fake data

        Parameters
        ----------
        total : `int`
            total objects to generate data
        random_activation : `bool`
            when it set to true data may have not be activate to show on website.
        batch_size : `int`
            this param uses to set how many data prepare bulk create in one query.
        disable_progress_bar : `bool`
            this param hidden `tqdm` package and skip calculating
            progress feature as well.

        Returns
        -------
        Tag Queryset
        """
        objs = [
            PostTag(
                title=word, slug=slugify(word), is_published=self.get_random_boolean()
            )
            for i in tqdm(range(total), disable=disable_progress_bar, colour="#b8835c")
            if (word := self.get_random_words(3))
        ]

        logger.debug("%d Tag Objects created successfully.", total)
        tags = PostTag.objects.bulk_create(objs, batch_size=batch_size)
        logger.debug("All Tags saved into database.")

        return tags

    def create_post_categories(
        self, total, random_activation=True, batch_size=300, disable_progress_bar=False
    ):
        """Create category fake data

        Parameters
        ----------
        total : `int`
            total objects to generate data
        random_activation : `bool`
            when it set to true data may have not be activate to show on website.
        batch_size : `int`
            this param uses to set how many data prepare bulk create in one query.
        disable_progress_bar : `bool`
            this param hidden `tqdm` package and skip
            calculating progress feature as well.

        Returns
        -------
        PostCategory Queryset
        """
        objs = [
            PostCategory(
                title=word, slug=slugify(word), is_published=self.get_random_boolean()
            )
            for i in tqdm(range(total), disable=disable_progress_bar, colour="#b8835c")
            if (word := self.get_random_words(3))
        ]

        logger.debug("%d post categories Objects created successfully.", total)
        PostCategory.objects.bulk_create(objs, batch_size=batch_size)
        logger.debug("post categories saved into database.")

        post_category = PostCategory.objects.all()
        return post_category

    def create_posts(
        self,
        total,
        tag_per_range=3,
        random_activation=True,  # noqa: W0613
        batch_size=300,
        disable_progress_bar=False,
    ):
        """Create post fake data

        Parameters
        ----------
        total : `int`
            total objects to generate data
        random_activation : `bool`
            when it set to true data may have not be activate
            to show on website.
        batch_size : `int`
            this param uses to set how many data prepare bulk
            create in one query.
        disable_progress_bar : `bool`
            this param hidden `tqdm` package and skip calculating
            progress feature as well.

        Returns
        -------
        Posts Queryset
        """

        post_categories = PostCategory.objects.all()
        tags = PostTag.objects.all()

        img_data, img_name, img_format = self.create_placeholder_image(
            1, subject="post_gallery"
        )
        banner_data, banner_name, banner_format = self.create_placeholder_image(
            1, size=(1980, 660), subject="post_banner"
        )
        objs = [
            Post(
                title=word,
                slug=slugify(word),
                summary=self.text.sentence()[:125],
                description=self.text.text(5),
                category=self.get_random_object(post_categories),
                is_published=self.get_random_boolean(),
                alternate_text=self.get_random_sentence()[:109],
                picture=SimpleUploadedFile(
                    name=img_name,
                    content=img_data,
                    content_type=f"image/{img_format.lower()}",
                ),
                banner=SimpleUploadedFile(
                    name=banner_name,
                    content=banner_data,
                    content_type=f"image/{banner_format.lower()}",
                ),
            )
            for i in tqdm(range(total), disable=disable_progress_bar, colour="#b8835c")
            if (word := self.get_random_words(3))
        ]

        logger.debug("%d post Objects created successfully.", total)
        Post.objects.bulk_create(objs, batch_size=batch_size)
        logger.debug("posts saved into database.")

        posts = Post.objects.all()

        list(
            tqdm(
                map(
                    functools.partial(self.add_to_m2m, tags, "tags", tag_per_range),
                    objs,
                )
            )
        )
        return posts

    def create_faqs(self, total, batch_size=300, disable_progress_bar=False):
        """Create FAQ fake data

        Parameters
        ----------
        total : `int`
            total objects to generate data
        batch_size : `int`
            this param uses to set how many data prepare bulk create in one query.
        disable_progress_bar : `bool`
            this param hidden `tqdm` package and skip calculating
            progress feature as well.

        Returns
        -------
        PostFaq Queryset
        """
        posts = Post.objects.all()

        objs = [
            PostFaq(
                question=self.get_random_sentence()[:150],
                answer=self.text.text(5),
                post=self.get_random_object(posts),
            )
            for i in tqdm(range(total), disable=disable_progress_bar, colour="#b8835c")
        ]

        logger.debug("%d FAQ Objects created successfully.", total)
        faqs = PostFaq.objects.bulk_create(objs, batch_size=batch_size)
        logger.debug("All FAQs saved into database.")

        return faqs
