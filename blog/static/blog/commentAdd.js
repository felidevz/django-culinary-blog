function hideShowCommentAdd(commentId) {
	const normalComment = document.getElementById('comment-add')
	const replyComment = document.getElementById('comment-add-reply-' + commentId)

	if (normalComment.style.display === 'none' && replyComment.style.display === 'block') {
		normalComment.style.display = 'block';
		replyComment.style.display = 'none';
	} else {
		normalComment.style.display = 'none';
		replyComment.style.display = 'block';
	}
}
