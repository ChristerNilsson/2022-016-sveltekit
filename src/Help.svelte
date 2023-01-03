<script>

	export let MAX_DOWNLOAD

	const helpTexts = []
	helpTexts.push("Separate words with a space or an underscore (_)")
	helpTexts.push("Search is case sensitive")
	helpTexts.push("Searching starts anywhere in a word")
	helpTexts.push("Number in parenthesis denotes number of images found")
	helpTexts.push("Search period like yyyy-mm-dd, yyyy-mm, yyyy or mm-dd")
	helpTexts.push("T = Tournament link")
	helpTexts.push("M = Member link")
	helpTexts.push("V = Video link")
	helpTexts.push("F = File link (pdf,mp4...)")
	helpTexts.push("[None] unmarks images")
	helpTexts.push(`[Download] zips up to ${MAX_DOWNLOAD} marked images`)
	helpTexts.push("[All] marks images")
	helpTexts.push("Home is the highest level directory")
	helpTexts.push("Ancestors are shown to the left of the Current directory")
	helpTexts.push("[Up] sets the Current directory to the closest ancestor")
	helpTexts.push("Directory selection is similar to Explorer")
	helpTexts.push("Clicking a directory, makes it the Current directory")
	helpTexts.push("Search is done in the subtree with the Current directory as root")
	helpTexts.push("Clicking a thumbnail shows a higher quality image")
	helpTexts.push("High quality images are draggable and zoomable")
	helpTexts.push("[Share] copies a URL to the clipboard")
	helpTexts.push("Sorting order: A B => (both A and B) or just A or just B")
	helpTexts.push("Sorting order: A B C => ABC AB AC BC A B C")
	helpTexts.push("Contact: janchrister punkt nilsson alfakrull gmail punkt com")
</script>

<div>
	{#each helpTexts as helpText}
		<div style="width:475px;">
			&nbsp; • {helpText}
		</div>
		{/each}
		<div style="width:475px;">
			<img class="center" src="./qr.png" alt="QR" style="width:200px;">
		</div>
	</div>

<style>
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 475px;
}
</style>
