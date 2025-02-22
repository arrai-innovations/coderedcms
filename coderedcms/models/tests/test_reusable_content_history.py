import json
import uuid

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from wagtail.blocks import StreamValue
from wagtail.test.utils import WagtailPageTests

from coderedcms.models import ReusableContent
from coderedcms.tests.testapp.models import WebPage


def get_value_from_content(content, indexes):
    if isinstance(content, StreamValue):
        value = content[indexes.pop(0)].value
    else:
        value = content[indexes.pop(0)]["value"]

    if indexes:
        value = get_value_from_content(value["content"], indexes=indexes)

    return value


class ReusableContentHistoryTestCase(WagtailPageTests):
    """
    Test that making changes to a reusable content will create
    a draft of any reusable content or pages that use it.
    """

    @csrf_exempt
    def setUp(self):
        super().setUp()

        # Use homepage
        self.homepage = WebPage.objects.get(url_path="/home/")

        # Create 3 reusable content objects.
        # We need to create these through the backend.
        self.rc1_content_uuid = str(uuid.uuid4())
        post_data = {
            "name": "Reusable1",
            "content-count": "1",
            "content-0-deleted": "",
            "content-0-order": "0",
            "content-0-type": "html",
            "content-0-id": self.rc1_content_uuid,
            "content-0-value": "<div>Reusable 1 - Test 1</div>",
        }
        add_url = reverse("wagtailsnippets_coderedcms_reusablecontent:add")
        self.client.post(add_url, data=post_data)
        self.rc1 = ReusableContent.objects.last()
        self.rc1_revision = self.rc1.revisions.last()

        self.rc2_content_uuid = str(uuid.uuid4())
        post_data = {
            "name": "Reusable2",
            "content-count": "1",
            "content-0-deleted": "",
            "content-0-order": "0",
            "content-0-type": "html",
            "content-0-id": self.rc2_content_uuid,
            "content-0-value": "<div>Reusable 2 - Test 1</div>",
        }
        add_url = reverse("wagtailsnippets_coderedcms_reusablecontent:add")
        self.client.post(add_url, data=post_data)
        self.rc2 = ReusableContent.objects.last()
        self.rc2_revision = self.rc2.revisions.last()

        key = "content-0-value-"
        post_data = {
            "name": "Reusable3",
            "content-count": "1",
            "content-0-deleted": "",
            "content-0-order": "0",
            "content-0-type": "row",
            "content-0-id": str(uuid.uuid4()),
            f"{key}settings-custom_template": "",
            f"{key}settings-custom_css_class": "",
            f"{key}settings-custom_id": "",
            f"{key}content-count": "1",
            f"{key}content-0-deleted": "",
            f"{key}content-0-order": "0",
            f"{key}content-0-type": "content",
            f"{key}content-0-id": str(uuid.uuid4()),
            f"{key}{key}settings-custom_template": "",
            f"{key}{key}settings-custom_css_class": "",
            f"{key}{key}settings-custom_id": "",
            f"{key}{key}settings-column_breakpoint": "md",
            f"{key}{key}column_size": "",
            f"{key}{key}content-count": "1",
            f"{key}{key}content-0-deleted": "",
            f"{key}{key}content-0-order": "0",
            f"{key}{key}content-0-type": "reusable_content",
            f"{key}{key}content-0-id": str(uuid.uuid4()),
            f"{key}{key}{key}settings-custom_template": "",
            f"{key}{key}{key}settings-custom_css_class": "",
            f"{key}{key}{key}settings-custom_id": "",
            f"{key}{key}{key}content": str(self.rc2.pk),
            f"{key}{key}{key}revision": "",
        }
        add_url = reverse("wagtailsnippets_coderedcms_reusablecontent:add")
        self.client.post(add_url, data=post_data)
        self.rc3 = ReusableContent.objects.last()
        self.rc3_revision = self.rc3.revisions.last()

        # Set the home page contents and save through the backend,
        # so we get a revision number created.
        body = "body-0-value-"
        key1 = "content-0-value-"
        key2 = "content-1-value-"
        post_data = {
            "next": "",
            "title": "Home",
            "cover_image": "",
            "body-count": "1",
            "body-0-deleted": "",
            "body-0-order": "0",
            "body-0-type": "row",
            "body-0-id": str(uuid.uuid4()),
            f"{body}settings-custom_template": "",
            f"{body}settings-custom_css_class": "",
            f"{body}settings-custom_id": "",
            f"{body}content-count": "1",
            f"{body}content-0-deleted": "",
            f"{body}content-0-order": "0",
            f"{body}content-0-type": "content",
            f"{body}content-0-id": str(uuid.uuid4()),
            f"{body}{key1}settings-custom_template": "",
            f"{body}{key1}settings-custom_css_class": "",
            f"{body}{key1}settings-custom_id": "",
            f"{body}{key1}settings-column_breakpoint": "md",
            f"{body}{key1}column_size": "",
            f"{body}{key1}content-count": "2",
            f"{body}{key1}content-0-deleted": "",
            f"{body}{key1}content-0-order": "0",
            f"{body}{key1}content-0-type": "reusable_content",
            f"{body}{key1}content-0-id": str(uuid.uuid4()),
            f"{body}{key1}{key1}settings-custom_template": "",
            f"{body}{key1}{key1}settings-custom_css_class": "",
            f"{body}{key1}{key1}settings-custom_id": "",
            f"{body}{key1}{key1}content": str(self.rc1.pk),
            f"{body}{key1}{key1}revision": "",
            f"{body}{key1}content-1-deleted": "",
            f"{body}{key1}content-1-order": "1",
            f"{body}{key1}content-1-type": "reusable_content",
            f"{body}{key1}content-1-id": str(uuid.uuid4()),
            f"{body}{key1}{key2}settings-custom_template": "",
            f"{body}{key1}{key2}settings-custom_css_class": "",
            f"{body}{key1}{key2}settings-custom_id": "",
            f"{body}{key1}{key2}content": str(self.rc2.pk),
            f"{body}{key1}{key2}revision": "",
            "tags": "",
            "custom_template": "coderedcms/pages/home_page.html",
            "index_num_per_page": "10",
            "index_order_by_classifier": "",
            "index_order_by": "",
            "related_num": "3",
            "related_classifier_term": "",
            "slug": "home",
            "seo_title": "",
            "search_description": "",
            "canonical_url": "",
            "og_image": "",
            "struct_org_type": "",
            "struct_org_name": "",
            "struct_org_logo": "",
            "struct_org_image": "",
            "struct_org_phone": "",
            "struct_org_address_street": "",
            "struct_org_address_locality": "",
            "struct_org_address_region": "",
            "struct_org_address_postal": "",
            "struct_org_address_country": "",
            "struct_org_geo_lat": "",
            "struct_org_geo_lng": "",
            "struct_org_hours-count": "0",
            "struct_org_actions-count": "0",
            "struct_org_extra_json": "",
            "comments-TOTAL_FORMS": "0",
            "comments-INITIAL_FORMS": "0",
            "comments-MIN_NUM_FORMS": "0",
            "comments-MAX_NUM_FORMS": "",
            "content_walls-count": "0",
            "go_live_at": "",
            "expire_at": "",
            "action-publish": "action-publish",
        }
        change_url = reverse(
            "wagtailadmin_pages:edit",
            args=(self.homepage.pk,),
        )
        self.client.post(change_url, data=post_data)
        self.homepage.refresh_from_db()
        self.homepage_revision = self.homepage.revisions.last()

    def tearDown(self):
        super().tearDown()

        self.client.logout()

        # Reset to not having body content, and delete the revisions.
        self.homepage.body = []
        self.homepage.save()
        self.homepage.revisions.all().delete()

        # Delete the reusable content objects and revisions we created.
        self.rc1.revisions.all().delete()
        self.rc2.revisions.all().delete()
        self.rc3.revisions.all().delete()
        self.rc1.delete()
        self.rc2.delete()
        self.rc3.delete()

    @csrf_exempt
    def test_single_level_reusable_content(self):
        """
        Tests to make sure the revisions are created correctly.
        """
        # We should have created 3 reusable content objects in setup.
        self.assertEqual(ReusableContent.objects.count(), 3)

        # The home page should be associated to reusable content 1 and 2
        # with revision numbers.
        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 0]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc1.pk)
        self.assertEqual(home_page_data["revision"], self.rc1_revision.pk)

        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 1]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc2.pk)
        self.assertEqual(home_page_data["revision"], self.rc2_revision.pk)

        # Save the reusable content 1 change form with a content change.
        post_data = {
            "name": "Reusable1",
            "content-count": 1,
            "content-0-deleted": "",
            "content-0-order": "0",
            "content-0-type": "html",
            "content-0-id": self.rc1_content_uuid,
            "content-0-value": "<div>Reusable 1 - Test 2</div>",
        }
        change_url = reverse(
            "wagtailsnippets_coderedcms_reusablecontent:edit",
            args=(self.rc1.pk,),
        )
        response = self.client.post(change_url, data=post_data)

        # We should be redirected back to the change list.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "wagtailsnippets_coderedcms_reusablecontent:list",
            ),
        )

        # We should have 2 revisions of reusable content 1.
        # #1 when the reusable content was created in setup.
        # #2 when we changed the data to Reusable 1 - Test 2.
        self.assertEqual(self.rc1.revisions.count(), 2)

        # We should have 3 revisions of the home page.
        # #1 when the home page was saved in setup.
        # #2 when we saved the reusable content change form for rc1.
        # #3 when the latest_revision is set on the home page.
        self.assertEqual(self.homepage.revisions.count(), 3)

        # The revision pk in the newest home page revision,
        # should match the new reusable content revision number.
        rc1_revision_pk = self.rc1.revisions.last().pk
        home_page_body = json.loads(
            self.homepage.revisions.last().content["body"]
        )
        home_page_data = get_value_from_content(
            home_page_body, indexes=[0, 0, 0]
        )
        self.assertEqual(home_page_data["content"], self.rc1.pk)
        self.assertEqual(home_page_data["revision"], rc1_revision_pk)

        # And the home page should still have the revision it previously
        # had, because the change form for the home page wasn't saved.
        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 0]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc1.pk)
        self.assertEqual(home_page_data["revision"], self.rc1_revision.pk)

        # Make sure when the reusable content is compared with
        # the previous version, that you see the changes.
        change_url = reverse(
            "wagtailsnippets_coderedcms_reusablecontent:revisions_compare",
            args=(self.rc1.pk, self.rc1_revision.pk, rc1_revision_pk),
        )
        response = self.client.get(change_url)

        # 1 should have been changed to 2.
        diff_content = (
            '<div class="comparison__child-object">&lt;div&gt;Reusable '
            '1 - Test <span class="deletion">1&lt;/div&gt;</span><span '
            'class="addition">2&lt;/div&gt;</span></div>'
        )
        self.assertInHTML(diff_content, response.content.decode("utf-8"))

        # Make sure when compared with the current version,
        # that you see the changes.
        self.homepage.refresh_from_db()
        change_url = reverse(
            "wagtailadmin_pages:revisions_compare",
            args=(self.homepage.pk, self.homepage_revision.pk, "latest"),
        )
        response = self.client.get(change_url)
        self.assertInHTML(diff_content, response.content.decode("utf-8"))

    @csrf_exempt
    def test_multi_level_reusable_content(self):
        """
        Tests to make sure the revisions are created correctly.
        """
        # We should have created 3 reusable content objects in setup.
        self.assertEqual(ReusableContent.objects.count(), 3)

        # The home page should be associated to reusable content 1 and 2
        # with revision numbers.
        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 0]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc1.pk)
        self.assertEqual(home_page_data["revision"], self.rc1_revision.pk)

        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 1]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc2.pk)
        self.assertEqual(home_page_data["revision"], self.rc2_revision.pk)

        # Save the reusable content 1 change form with a content change.
        post_data = {
            "name": "Reusable2",
            "content-count": 1,
            "content-0-deleted": "",
            "content-0-order": "0",
            "content-0-type": "html",
            "content-0-id": self.rc2_content_uuid,
            "content-0-value": "<div>Reusable 2 - Test 2</div>",
        }
        change_url = reverse(
            "wagtailsnippets_coderedcms_reusablecontent:edit",
            args=(self.rc2.pk,),
        )
        response = self.client.post(change_url, data=post_data)

        # We should be redirected back to the change list.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(
                "wagtailsnippets_coderedcms_reusablecontent:list",
            ),
        )

        # We should have 2 revisions of reusable content 2.
        # #1 when the reusable content was created in setup.
        # #2 when we changed the data to Reusable 2 - Test 2.
        self.assertEqual(self.rc2.revisions.count(), 2)

        # We should have 3 revisions of reusable content 3.
        # #1 when the reusable content was created in setup.
        # #2 when we saved the reusable content change form for rc2.
        # #3 when the latest_revision is set on rc3.
        self.assertEqual(self.rc3.revisions.count(), 3)

        # We should have 3 revisions of the home page.
        # #1 when the home page was saved in setup.
        # #2 when we saved the reusable content change form for rc2.
        # #3 when the latest_revision is set on the home page.
        self.assertEqual(self.homepage.revisions.count(), 3)

        # The revision pk in the newest rc3 revision, should
        # match the new reusable content revision number.
        rc2_revision_pk = self.rc2.revisions.last().pk
        rc3_content = json.loads(self.rc3.revisions.last().content["content"])
        rc3_data = get_value_from_content(rc3_content, indexes=[0, 0, 0])
        self.assertEqual(rc3_data["content"], self.rc2.pk)
        self.assertEqual(rc3_data["revision"], rc2_revision_pk)

        # And rc3 should still have the revision it previously
        # had, because the change form for rc3 wasn't saved.
        rc3_data = get_value_from_content(self.rc3.content, indexes=[0, 0, 0])
        self.assertEqual(rc3_data["content"].pk, self.rc2.pk)
        self.assertEqual(rc3_data["revision"], self.rc2_revision.pk)

        # The revision pk in the newest home page revision,
        # should match the new reusable content revision number.
        rc2_revision_pk = self.rc2.revisions.last().pk
        home_page_body = json.loads(
            self.homepage.revisions.last().content["body"]
        )
        home_page_data = get_value_from_content(
            home_page_body, indexes=[0, 0, 1]
        )
        self.assertEqual(home_page_data["content"], self.rc2.pk)
        self.assertEqual(home_page_data["revision"], rc2_revision_pk)

        # And the home page should still have the revision it previously
        # had, because the change form for the home page wasn't saved.
        home_page_data = get_value_from_content(
            self.homepage.body, indexes=[0, 0, 1]
        )
        self.assertEqual(home_page_data["content"].pk, self.rc2.pk)
        self.assertEqual(home_page_data["revision"], self.rc2_revision.pk)

        # Make sure when the reusable content is compared with
        # the previous version, that you see the changes.
        change_url = reverse(
            "wagtailsnippets_coderedcms_reusablecontent:revisions_compare",
            args=(self.rc2.pk, self.rc2_revision.pk, rc2_revision_pk),
        )
        response = self.client.get(change_url)

        # 1 should have been changed to 2.
        diff_content = (
            '<div class="comparison__child-object">&lt;div&gt;Reusable '
            '2 - Test <span class="deletion">1&lt;/div&gt;</span><span '
            'class="addition">2&lt;/div&gt;</span></div>'
        )
        self.assertInHTML(diff_content, response.content.decode("utf-8"))

        # Make sure when rc3 is compared with the current version,
        # that you see the changes.
        self.rc3.refresh_from_db()
        change_url = reverse(
            "wagtailsnippets_coderedcms_reusablecontent:revisions_compare",
            args=(self.rc3.pk, self.rc3_revision.pk, "latest"),
        )
        response = self.client.get(change_url)
        self.assertInHTML(diff_content, response.content.decode("utf-8"))

        # Make sure when the home page is compared with the current version,
        # that you see the changes.
        self.homepage.refresh_from_db()
        change_url = reverse(
            "wagtailadmin_pages:revisions_compare",
            args=(self.homepage.pk, self.homepage_revision.pk, "latest"),
        )
        response = self.client.get(change_url)
        self.assertInHTML(diff_content, response.content.decode("utf-8"))
